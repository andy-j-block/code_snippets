#####################
#
# multi_ROC_w_StratKFold
# written by: Andy Block
# date: Feb 20, 2021
#
#####################
#
# This function creates plots of the ROC curves for a list of classifiers side by side.
# The X and y are split via Stratified K Fold cross validation.
# The classifiers and theirs names should be passed in as lists, respective of order.
# For instance, if your classifiers are called [clf_svc, clf_randfor], 
# the classifier names would be ['Support Vector Classifier', 'Random Forest'].
#
# It is based off of the Receiver Operating Characteristic (ROC) with cross validation example found here: 
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html#sphx-glr-auto-examples-model-selection-plot-roc-crossval-py
#
#####################

from matplotlib import pyplot as plt
import numpy as np


def multi_ROC_w_StratKFold(X, y, K, classifiers, classifier_names):
    
    cv = StratifiedKFold(n_splits=K)
    
    # initialize several dictionaries that will be populated by classifier
    # e.g. the tprs dictionary will have the true positive rates for each K fold across the fpr_range (X-axis)
    tprs = {}
    aucs = {}
    mean_tprs = {}
    mean_auc = {}
    std_auc = {}

    fpr_range = np.linspace(0, 1, 100) # X-axis range
    
    # create the subplot
    num_axes = len(classifiers)
    fig, axs = plt.subplots(1, num_axes, figsize=(10*num_axes,10))


    for i, classifier in enumerate(classifiers):

        interp_tprs = []
        roc_aucs = []

        for j, (train, test) in enumerate(cv.split(X, y)):
            
            classifier.fit(X.iloc[train], y.iloc[train])

            viz = plot_roc_curve(clf_svc, X.iloc[test], y.iloc[test],
                                 name='ROC fold {}'.format(j),
                                 alpha=0.3, lw=1, ax=axs[i])
            
            # interpolate the true and false pos values across the X range
            interp_tpr = np.interp(fpr_range, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            interp_tprs.append(interp_tpr)
            
            # store the AUC for each K fold
            roc_aucs.append(viz.roc_auc)
            
        # store the TPRs and AUCs by classifier for the all K folds in their dictionaries
        tprs[classifier] = interp_tprs
        aucs[classifier] = roc_aucs

        
        # plot dotted line from (0,0) to (1,1)
        axs[i].plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
            label='Chance', alpha=.8)
        
        
        # calculate mean TPRs and mean and std AUCs by classifier and plot
        mean_tprs[classifier] = np.mean(tprs[classifier], axis=0)
        mean_tprs[classifier][-1] = 1.0

        mean_auc[classifier] = auc(fpr_range, mean_tprs[classifier])
        std_auc[classifier] = np.std(aucs[classifier])

        axs[i].plot(fpr_range, mean_tprs[classifier], color='b',
                label=r'Mean ROC (AUC = %0.3f $\pm$ %0.3f)' % (mean_auc[classifier], std_auc[classifier]),
                lw=2, alpha=.8)
        

        # shade the area 1 std below and above
        std_tpr = np.std(tprs[classifier], axis=0)
        tprs_upper = np.minimum(mean_tprs[classifier] + std_tpr, 1)
        tprs_lower = np.maximum(mean_tprs[classifier] - std_tpr, 0)

        axs[i].fill_between(fpr_range, tprs_lower, tprs_upper, color='grey', alpha=.2,
                        label=r'$\pm$ 1 std. dev.')
        

        # a bit of formatting
        axs[i].set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
               title="ROC Curve: {}".format(classifier_names[i]))
        axs[i].legend(loc="lower right")

    plt.show()