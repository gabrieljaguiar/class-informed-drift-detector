# CIDDM: Class Informed Concept Drift Detector Method

## Abstract
Dynamic environments pose significant challenges to machine learning models due to the presence of concept drift, wherein the underlying data distribution evolves over time. Moreover, concept drift can affect only a subset of classes globally or locally. In response to this challenge, this paper introduces a novel approach, referred to as the Class Informed Drift Detection Method (CIDDM), designed to detect and respond to concept drifts in multi-class data streams. CIDDM leverages statistical descriptors and class-specific information to precisely identify both local and global concept drifts. Through rigorous and extensive experimentation and comparison with $11$ state-of-the-art methods, the proposed drift detector demonstrates superior performance in detecting concept drifts, particularly in scenarios with local changes within the data stream. Moreover, CIDDM's classifier-agnostic nature ensures its adaptability across diverse learning models. Furthermore, we investigate the impact of combining drift detectors and classifiers on predictive performance. The results of this study validate CIDDM's efficacy in detecting concept drift and therefore enhancing the resilience of machine learning systems to concept drift, thereby advancing the field of stream learning and bolstering the reliability of machine learning applications in dynamic environments.

<table>
  <tr>
    <td valign="top"><img src="figures/scatter_HT.jpg"></td>
    <td valign="top"><img src="figures/scatter_NB.jpg"></td>
  </tr>
 </table>

## Implementation detailes

CIDDM class is implemented in the file `drift_detectors/multi_class_detector.py`.
The drift detector was implemented in Python 3.8 using river package. 

## Reference

Manuscript was submitted to Data Mining and Knowledge Discovery journal and pre-print is available at [arxiv](XXXX)

```
@misc{aguiar2023local,
  author={Aguiar, Gabriel and Cano, Alberto},
  title={CIDDM: Class Informed Concept Drift Detector Method},
  year={2024},
  eprint={2311.06396},
  archivePrefix={arXiv},
  primaryClass={cs.LG}
}
```
