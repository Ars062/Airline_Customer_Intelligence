# Recommended-prediction model (VERIFIED run)

Best by F1: **logistic_regression**

- dummy_stratified: acc=0.5193 prec=0.4001 rec=0.4002 F1=0.4002 ROC-AUC=0.4996
- logistic_regression: acc=0.9524 prec=0.9403 rec=0.9408 F1=0.9406 ROC-AUC=0.9892
- linear_svc: acc=0.9452 prec=0.9301 rec=0.9334 F1=0.9317 ROC-AUC=0.9861
- complement_nb_textonly: acc=0.865 prec=0.7948 rec=0.8937 F1=0.8413 ROC-AUC=0.9392

Trade-offs: LinearSVC/LogReg use full features; ComplementNB is text-only (weaker but deployable on review text alone). Dummy shows the 60/40-majority floor. F1 chosen over accuracy because recommending correctly for the minority class matters and accuracy would reward majority-class bias.
