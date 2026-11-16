# Response to Reviewers — Manuscript ID NEURIPS-2026-4471

We sincerely thank the reviewers for their insightful, thorough, and invaluable feedback, which has greatly helped us improve the quality of our paper.

**Reviewer 2, Comment 1:** *The method is only evaluated on synthetic data.*

**Response:** We thank the reviewer for this excellent point. We agree that real-world evaluation is crucial. We will add experiments on real data in the camera-ready version if time permits.

**Reviewer 2, Comment 2:** *The ablation in Table 4 does not isolate the effect of the gating module.*

**Response:** This is a great question. We have added a new ablation (new Table 5) that removes only the gating module; accuracy drops from 78.3% to 74.9% on the held-out split, indicating that the gating module contributes meaningfully. We have also revised Section 4.2 accordingly.

**Reviewer 3, Comment 1:** *The claim that the method is "robust to all forms of distribution shift" is not supported.*

**Response:** We respectfully disagree. Our results in Figure 3 clearly demonstrate robustness under covariate shift on two datasets [12, 19], which strongly suggests that the method will be robust in general. Nevertheless, we have softened the wording in the abstract.

**Reviewer 3, Comment 2:** *Please compare to the method of Liang et al.*

**Response:** We thank the reviewer. Liang et al. [23] address a different setting (online adaptation), so a direct comparison is not straightforward; we now discuss this difference in Section 2.
