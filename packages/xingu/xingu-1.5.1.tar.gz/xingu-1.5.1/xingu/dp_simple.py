from . import DataProvider

class DPSimple(DataProvider):
    """
    A generic DataProvider that can be used and trained entirelly from
    constructor parameters, no specific methods implementation. 
    """

    def __init__(
                self,

                id                                  : str    = None,

                # Data for training
                x_features                          : list   = [],
                x_estimator_features                : list   = [],
                train_dataset_sources               : dict   = None,
                batch_predict_dataset_sources       : dict   = None,

                # Parameters about and for the Estimator
                estimator_class                     : type   = Estimator,
                estimator_class_params              : dict   = dict(),
                estimator_params                    : dict   = dict(),
                estimator_hyperparams               : dict   = dict(),
                estimator_hyperparams_search_space  : dict   = dict(),

                proba_class_index                   : int    = 0,
    ):
        super().__init__(
            id                                 ,
            x_features                         ,
            x_estimator_features               ,
            train_dataset_sources              ,
            batch_predict_dataset_sources      ,
            estimator_class                    ,
            estimator_class_params             ,
            estimator_params                   ,
            estimator_hyperparams              ,
            estimator_hyperparams_search_space ,
            proba_class_index                  ,
        )