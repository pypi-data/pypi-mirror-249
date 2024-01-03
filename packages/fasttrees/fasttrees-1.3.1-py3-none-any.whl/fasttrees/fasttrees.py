'''Fast-and-frugal tree classifier
'''
from __future__ import annotations

import operator
import logging
import itertools
import warnings
from typing import Callable, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_is_fitted, check_X_y, check_array
from sklearn.metrics._scorer import balanced_accuracy_score




# pylint: disable=too-many-instance-attributes,too-many-arguments
class FastFrugalTreeClassifier(BaseEstimator, ClassifierMixin):
    """Fast-and-Frugal-Tree classifier

        Inits Fast-and-Frugal-Tree classifier.

        Parameters
        ----------
        construction_algorithm : str, default='marginal_fan'
            Specifies the algorithm used to create trees. Currently only supports 'marginal_fan'.

        scorer : func, default=sklearn.metrics.scorer.balanced_accuracy_score
            Specifies the metric to maximize when choosing threshold. Any function that returns
            higher values for better predictions.

        max_levels : int
            Specifies the maximum number of levels for possible trees.

        stopping_param : float
            Specifies the prune levels containing less than ``stopping_param`` of cases.

        max_categories : int
            Specifies the maximum number of categories to group together for categorical columns.

        max_cuts : int
            Specifies the maximum number of cuts to try on a numerical column.

        Examples
        ----------
        >>> from fasttrees.fasttrees import FastFrugalTreeClassifier
        >>> from sklearn.datasets import make_classification
        >>> X, y = make_classification(n_features=4, random_state=0)
        >>> fc = FastFrugalTreeClassifier
        >>> fc.fit(X, y)
        >>> fc.get_tree()
    """

    _construction_algorithms = ['marginal_fan']

    _operator_dict = {
        '<=': operator.le,
        '>': operator.gt,
        '==': operator.eq,
        'in': lambda val, lst: val in lst
    }

    def __init__(
        self,
        construction_algorithm: str='marginal_fan',
        scorer: Callable[[], float]=balanced_accuracy_score,
        max_levels: int=4,
        stopping_param: float=.1,
        max_categories: int=4,
        max_cuts: int=100
    ) -> None:
        self.construction_algorithm = construction_algorithm
        self.scorer = scorer
        self.max_levels = max_levels
        self.stopping_param = stopping_param
        self.max_categories = max_categories
        self.max_cuts = max_cuts

    def _more_tags(self):
        """Add tags to categories the classifier, which is used by sklearn tests,
        e.g. to decide which tests to run.
        """
        return {
            'binary_only': True
        }

    def _score(self, y: pd.DataFrame, predictions: pd.DataFrame, sample_weight=None) -> float:
        """
        Return the score on the given ``y`` and ``predictions``.

        Parameters
        ----------
            y : pandas.DataFrame
                The real outcomes.

            predictions : pandas.DataFrame
                The predicted outcomes.

            sample_weight : array-like of shape (n_samples,), default=None
                Sample weights.

        Returns
        ----------
            score : float
                The score w.r.t. ``y``.
        """
        return self.scorer(y, predictions, sample_weight=sample_weight)

    def _get_thresholds(self, X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        """
        Get possible thresholds and directions for each feature.

        Parameters
        ----------
            X : pandas.DataFrame
                The test samples as a Dataframe with features as columns. Features can be
                numerical or categorical.
            y : pandas.DataFrame
                The true labels for ``X```, which are real, or binary, outcomes.

        Returns
        ----------
            self.all_thresholds_ : pandas.DataFrame
                A dataframe with rows for every feature, with threshold, direction and scorer.
        """
        midx = pd.MultiIndex(levels=[[], []],
                             labels=[[], []],
                             names=['cue_nr', 'threshold_nr'])
        threshold_df = pd.DataFrame(
            columns=['feature', 'direction', 'threshold', 'type', self.scorer.__name__],
            index=midx)

        # Get optimal classification threshold for each feature
        for i, col in enumerate(X):
            logging.debug('Get threshold for %s', col)
            j = 0

            if X[col].dtype.name == 'category':
                # categorical
                categories = X[col].cat.categories

                threshold_df['threshold'] = threshold_df['threshold'].astype(object)

                # try all possible subsets of categories

                for l in range(1, min(len(categories), self.max_categories + 1)):
                    for subset in itertools.combinations(categories, l):
                        predictions = X[col].isin(subset)
                        metric = self._score(y, predictions)

                        # save metric, direction and threshold
                        threshold_df.at[(i, j), 'direction'] = 'in'
                        threshold_df.at[(i, j), 'threshold'] = subset
                        threshold_df.at[(i, j), self.scorer.__name__] = metric
                        j += 1

                threshold_df.loc[i, 'type'] = 'categorical'
            else:
                # numerical
                percentiles = np.linspace(0, 100, self.max_cuts + 1)

                test_values = np.percentile(X[col], percentiles)

                # try smaller than and bigger than for every unique value in column
                for val in test_values:
                    for direction, _operator in {
                            op: self._operator_dict[op] for op in ['<=', '>']}.items():
                        predictions = _operator(X[col], val)
                        metric = self._score(y, predictions)

                        threshold_df.at[(i, j), 'threshold'] = val
                        threshold_df.at[(i, j), 'direction'] = direction
                        threshold_df.at[(i, j), self.scorer.__name__] = metric
                        j += 1

                threshold_df.loc[i, 'type'] = 'numerical'

            threshold_df.loc[i, 'feature'] = col

        threshold_df[self.scorer.__name__] = threshold_df[self.scorer.__name__].astype(float)

        # sort features by their score
        self.all_thresholds_ = threshold_df

    def _get_best_thresholds(self):
        """
        Get thresholds and directions that maximimize scorer for each feature.

        Returns
        ----------
            self.thresholds_ : pandas.DataFrame
                A dataframe with rows for every feature, with threshold, direction and
                scorer, sorted by scorer.
        """
        threshold_df = pd.DataFrame(
            columns=['feature', 'direction', 'threshold', 'type', self.scorer.__name__])
        for cue_nr, cue_df in self.all_thresholds_.groupby(level=0):
            idx = cue_df[self.scorer.__name__].idxmax()
            threshold_df.loc[cue_nr,
                             ['feature', 'direction', 'threshold', 'type', self.scorer.__name__
                            ]] = cue_df.loc[idx]

        threshold_df[self.scorer.__name__] = threshold_df[self.scorer.__name__].astype(float)

        self.thresholds_ = (threshold_df
            .sort_values(by=self.scorer.__name__, ascending=False)
            .reset_index(drop=True)
        )

    def _predict_all(self, X: pd.DataFrame, cue_df: pd.DataFrame) -> pd.Series:
        """
        Make predictions for ``X`` given ``cue_df``.

        Parameters
        ----------
            X : pandas.Dataframe
                The input samples as a dataframe with features as columns. Features can be
                numerical or categorical.

            cue_df : pandas.Dataframe
                A dataframe with ordered features, directions, thresholds, and exists.

        Returns
        ----------
            all_predictions : pandas.Series
                A series with a prediction for every cue in cue_df up to the point where the
                fast-and-frugal-tree was exited.
        """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
            X.columns = [f'A{id}' for id in X.columns]

        nr_rows = cue_df.shape[0]

        # could be replaced with logical expression which would not have to be applied row-wise?
        # currently very slow
        def prediction_func(row):
            """
            Makes a prediction for the given feature row.

            Look up the row's features in order of their score. Exit if the threshold is met and
            the tree exits on True, or if the threshold is not met and the tree exits on False.

            Parameters
            ----------
                row : dict
                    A dict with the features.

            Returns
            ----------
                ret_ser : pandas.Series
                    A series with a prediction for all cues used.
            """
            ret_ser = pd.Series()
            for index, cue_row in cue_df.iterrows():
                _operator = self._operator_dict[cue_row['direction']]
                outcome = _operator(row[cue_row['feature']], cue_row['threshold'])

                # store prediction in series
                ret_ser.set_value(index, outcome)

                # exit tree if outcome is exit or last cue reached
                if (cue_row['exit'] == int(outcome)) or (index + 1 == nr_rows):
                    break

            # return predictions for cues used
            return ret_ser

        all_predictions = X.apply(prediction_func, axis=1)
        return all_predictions

    @staticmethod
    def _get_final_prediction(all_predictions: pd.DataFrame) -> pd.DataFrame:
        """
        Get final (latest non-null) predictions from all cue predictions.

        Parameters
        ----------
            all_predictions : pandas.Dataframe
               A dataframe with all predictions.

        Returns
        ----------
            final_prediction : pandas.DataFrame
                A data frame with the final predictions.
        """
        return all_predictions.ffill(axis=1).iloc[:, -1]

    def _predict_and_prune(
            self,
            X: pd.DataFrame,
            cue_df: pd.DataFrame
        ) -> Tuple:
        """
        Make predictions and prune features that classify less than ``self.stopping_param``.

        Parameters
        ----------
            X : pandas.Dataframe
                The training input samples with features as columns. Features can be
                numerical or categorical.

        Returns
        ----------
            Tuple
                A tuple of length three where the first element are the predictions, the second
                element are the nr cused used, and the third ond are the fraction used.
        """
        logging.debug('Predicting ...')
        all_predictions = self._predict_all(X, cue_df)

        # prune non classifying features
        logging.debug('Pruning ...')
        fraction_used = all_predictions.notnull().mean()

        cols = [col for col in all_predictions if fraction_used[col] >= self.stopping_param]

        all_predictions = all_predictions[cols]
        fraction_used = fraction_used[:len(cols)]

        # get last prediction
        predictions = self._get_final_prediction(all_predictions)

        nr_cues_used = len(cols)

        return predictions, nr_cues_used, fraction_used

    def _growtrees(self, X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        """
        Grow all possible trees up to ``self.max_levels``. Levels that classify less than 
        ``self.stopping_param`` are pruned.

        Parameters
        ----------
            X : pandas.Dataframe
                The training input samples with features as columns. Features can be numerical
                or categorical.

            y : pandas.Dataframe
                The target class labels as real or binary outcomes.

        Returns
        ----------
            self.all_trees_ : pandas.DataFrame
                A dataframe with all trees grown.
        """
        relevant_features = self.thresholds_.head(self.max_levels)
        midx = pd.MultiIndex(levels=[[], []],
                             labels=[[], []],
                             names=['tree', 'idx'])
        tree_df = pd.DataFrame(
            columns=['feature', 'direction', 'threshold',
                     'type', self.scorer.__name__, 'fraction_used'],
            index=midx)

        for tree in range(2 ** (self.max_levels - 1)):
            logging.debug('Grow tree %s ...', tree)
            for index, feature_row in relevant_features.iterrows():
                tree_df['threshold'] = tree_df['threshold'].astype(object)

                tree_df.loc[
                    (tree, index),
                    ['feature', 'direction', 'threshold', 'type', self.scorer.__name__]
                ] = feature_row

                # exit 0.5 is stop, exit 1 means stop on true, exit 0 means stop on false
                tree_df.loc[(tree, index), 'exit'] = np.binary_repr(
                    tree, width=self.max_levels)[-1 - index]

            tree_df['exit'] = tree_df['exit'].astype(float)

            predictions, nr_cues_used, fraction_used = self._predict_and_prune(X, tree_df.loc[tree])

            for i in range(nr_cues_used, len(relevant_features)):
                tree_df.drop(index=(tree, i), inplace=True)

            tree_df.loc[tree, 'fraction_used'] = fraction_used.values
            tree_df.loc[(tree, nr_cues_used - 1), 'exit'] = 0.5

            score = self._score(y, predictions)
            logging.debug('Score is %s ...', score)
            tree_df.loc[tree, self.scorer.__name__] = score

        self.all_trees_ = tree_df

    def get_tree(self, idx: int=None, decision_view: bool=True) -> pd.DataFrame:
        """Get tree with index ``idx`` from all trees.

        Retrieves the tree with index ``idx``, which is especially useful if the predictions
        will be carried out by humans, or communication purposes, e.g. presentations.

        Parameters
        ----------
            idx : int, Default=None
                The index of the desired tree. Default is None, which returns the best tree.

            decision_view : bool, default=True
                If true, it will return a dataframe in an easily readable form, which can then
                be used to make a quick decision. If false, it will return the original dataframe
                with more statistics. The default is ``True``.

        Returns
        ----------
            tree_df : pandas.DataFrame
                The dataframe of the tree with index ``idx``.
        """
        if idx is None:
            idx = self.all_trees_[self.scorer.__name__].idxmax()[0]

        tree_df = self.all_trees_.loc[idx]

        if decision_view:
            def exit_action(exit_value):
                ret_ser = pd.Series()
                ret_ser.set_value('IF YES', '↓')
                ret_ser.set_value('IF NO', '↓')
                if exit_value <= 0.5:
                    ret_ser.set_value('IF NO', 'decide NO')
                if exit_value >= 0.5:
                    ret_ser.set_value('IF YES', 'decide YES')
                return ret_ser

            tree_df = pd.concat([tree_df, tree_df['exit'].apply(exit_action)], axis=1)
            tree_df = tree_df[['IF NO', 'feature', 'direction', 'threshold', 'IF YES']]

        return tree_df

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> FastFrugalTreeClassifier:
        """
        Builds the fast and frugal tree classifier from the training set (X, y).

        Parameters
        ----------
            X : pandas.Dataframe
                The training input samples with features as columns. Features can be
                numerical or categorical.

            y : pandas.Dataframe
                The target class labels as real or binary outcomes.

        Returns
        ----------
            self : FastFrugalTreeClassifier
                Fitted estimator.
        """
        self._validate_hyperparameters()

        check_X_y(X, y, dtype=None, accept_sparse=False)

        try:
            if not isinstance(X, pd.DataFrame):
                X = np.array(X)

            if not isinstance(y, pd.DataFrame):
                y = np.array(y)
        except:
            raise ValueError('Failed to convert X or Y to numpy arrays')


        if isinstance(X, np.ndarray):
            X = X.astype(np.float) if X.dtype == object else X

            X = pd.DataFrame(X)
            X.columns = [f'A{id}' for id in X.columns]

        if isinstance(y, np.ndarray):
            y = pd.DataFrame(y)
            y.columns = ['y']



        if len(unique_labels(y)) > 2:
            raise ValueError(f'Fast and frugal trees are binary classification models, but '\
                             f'the training data has the {len(unique_labels(y))} labels '\
                             f'{unique_labels(y)}')

        if len(unique_labels(y)) == 1:
            raise ValueError('Only one class in training data.')

        y_unique = unique_labels(y)
        _y_map = {y_unique[0]: False, y_unique[1]: True}
        _y_map_rev = {value: key for key, value in _y_map.items()}
        _y = np.array([_y_map[el] for el in y['y']])

        self._get_thresholds(X, _y)
        self._get_best_thresholds()
        self._growtrees(X, _y)
        self.best_tree_ = self.get_tree()

        # store the training data set seen during training
        self.classes_ = unique_labels(y)
        self.X_ = X
        self.y_ = y
        self._y = _y
        self._y_map = _y_map
        self._y_map_rev = _y_map_rev
        return self

    def _validate_hyperparameters(self) -> None:
        # validate types
        if not isinstance(self.construction_algorithm, str):
            raise ValueError(f'construction_algorithm is not a str, '\
                             f'got type {type(self.construction_algorithm)}')

        if not isinstance(self.scorer, Callable):
            raise ValueError(f'scorer must be a callable, '\
                             f'got type {self.scorer}')

        if not isinstance(self.max_levels, int):
            raise ValueError(f'max_levels must be an int, '\
                             f'got type {type(self.max_levels)}')

        if not isinstance(self.stopping_param, float):
            raise ValueError(f'stopping_param must be a float, '\
                             f'got type {type(self.stopping_param)}')

        if not isinstance(self.max_categories, int):
            raise ValueError(f'max_categories must be an int, '\
                             f'got type {type(self.max_categories)}')

        if not isinstance(self.max_cuts, int):
            raise ValueError(f'max_cuts must be an int, '\
                             f'got type {type(self.max_cuts)}')


        # validate input range
        if self.construction_algorithm not in self._construction_algorithms:
            raise ValueError(f'Construction algorithm {self.construction_algorithm} is not '\
                             f'supported. Supported construction algorithms are '\
                             f'{self._construction_algorithms}')

    def predict(self, X: pd.DataFrame, tree_idx: int=None) -> pd.DataFrame:
        """
        Predict class value for ``X``.

        Returns the predicted class for each sample in ``X``.

        Parameters
        ----------
            X : pandas.DataFrame
                The input samples as a Dataframe with features as columns. Features can be
                numerical or categorical.

            tree_idx : int, default=None
                The tree to use for the predictions. Default is best tree.

        Returns
        ----------
           y : pandas.DataFrame
                The predicted classes.
        """
        check_is_fitted(self, ['X_', 'y_'])
        check_array(X, dtype=None, accept_sparse=True)

        try:
            if not isinstance(X, pd.DataFrame):
                X = np.array(X)
        except:
            raise ValueError('Failed to convert X to numpy arrays')

        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
            X.columns = [f'A{id}' for id in X.columns]

        if self.X_.shape[1] != X.shape[1]:
            raise ValueError(f'The number of features in X is differs from the number of '\
                             f'features in fit. Fit was called with {self.X_.shape[1]} features, '\
                             f'but X has {X.shape[1]} features.')

        all_predictions = self._predict_all(X, self.get_tree(tree_idx, decision_view=False))
        final_prediction = self._get_final_prediction(all_predictions)
        return np.array([self._y_map_rev[el] for el in final_prediction])

    def score(self, X: pd.DataFrame, y: pd.DataFrame=None, sample_weight=None) -> float:
        """
        Predicts for data X. Scores predictions against y.

        Parameters
        ----------
            X : pandas.DataFrame
                The test samples as a Dataframe with features as columns. Features can be
                numerical or categorical.

            y : pandas.DataFrame, default=None
                The true labels for ``X```.

            sample_weight : array-like of shape (n_samples,), default=None
                Sample weights.

        Returns
        ----------
            score : float
                The score of ``self.predict(X)`` w.r.t ``y``.
        """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
            X.columns = [f'A{id}' for id in X.columns]

        if isinstance(y, np.ndarray):
            y = pd.DataFrame(y)
            y.columns = ['y']

        return self._score(y, self.predict(X), sample_weight=None)

    def in_words(self, idx: int=None) -> str:
        """``in_words`` generates a verbal description of the fast-and-frugal tree (FFT) from the
        fast-and-frugal tree with index ``idx``.

        Parameters
        ----------
            idx : int, Default=None
                The index of the desired tree. Default is None, which selects the best tree.

        Returns
        -------
            words : str.
                A string describing the tree in words.
        """
        warnings.warn(f'{self.in_words} is not thoroughly tested. Use the function with '\
                      f'suspicion.')

        words = ''

        for row in self.get_tree(idx=idx, decision_view=True).itertuples(index=False):
            if row[4] != '↓' and row[0] == '↓':
                words += f'If {row[1]} {row[2]} {row[3]}, '\
                         f'{row[4]}\n'
            else:
                words += f'If not {row[1]} {row[2]} {row[3]}, '\
                         f'{row[0]}\n'

            if row[0] != '↓' and row[4] != '↓':
                words += f'If {row[1]} {row[2]} {row[3]}, '\
                         f'{row[0]}, otherwise, {row[4]}\n'

        return words
