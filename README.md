# fish_freshness_detection

## Introduction
The exponential growth of aquaculture in recent years has sparked a surge in demand for fish products, underscoring the necessity for ensuring their purity. Fish freshness stands as a pivotal factor in evaluating quality, profoundly impacting consumer satisfaction. Fishing techniques, handling practices, packaging, and storage methodologies all exert influence on the shelf life of harvested fish. Despite various cooling and preservation techniques aimed at extending shelf life, post-mortem changes in fish physiology pose formidable challenges to maintaining freshness. Policy analysts and scientists globally prioritize the freshness, safety, and security of seafood products, recognizing their critical importance in public health and economic stability. A myriad of methods have been devised to evaluate fish freshness, including sensory-based approaches, microbial analysis, chemical assays, and physical measurements. While each method offers unique advantages, they also present limitations in terms of cost, time, and destructiveness.

Image processing techniques have emerged as a non-destructive and efficient means of evaluating fish freshness, offering insights into variations in color, texture, and structural attributes. Recent advancements have seen the integration of computer vision with spectroscopy, near-infrared imaging, and electronic nose technology, enhancing the comprehensiveness of freshness assessment. However, despite the array of available methods, there remains a need for efficient, accurate, and practical techniques suitable for real-world applications in the fisheries industry. This study proposes leveraging image processing techniques with a focus on skin tissue as the region of interest to develop a complementary method that has the potential to enhance freshness evaluation. By analyzing statistical features of skin tissue and understanding degradation patterns in fish images, the proposed framework aims to automate the screening procedure, contributing to more efficient and reliable fish freshness identification.

## Proposed Methodology
This research presents an innovative approach for automatically detecting fish freshness, focusing on computational efficiency and non-destructiveness, specifically emphasizing the analysis of skin tissue. The methodology begins with recognizing early degradation symptoms in the appearance of fish skin, such as loss of brightness and shine, which are indicative of freshness decline. Skin tissue is chosen as the primary region of interest due to its prominent role in reflecting freshness alterations. The proposed method employs image processing techniques, including segmentation of the skin region and extraction of statistical features, to interpret variations in skin appearance. Experimental results validate the effectiveness and non-destructiveness of the proposed methodology in detecting freshness based on extracted textural features from the skin tissue.

### I. Image Acquisition
This study focuses on Nagarai, commonly known as Red Snapper, a prized fish indigenous to the marine waters of Southern India. Renowned for its exquisite taste, Nagarai is highly sought after in coastal regions worldwide. Belonging to the genus Lutjanus and the family Lutjanidae, this fish boasts a sleek body adorned with seven fins and scales, except for its fins and head. With vibrant hues of red or pink on its dorsal side and a silvery belly, Nagarai possesses a distinctive appearance characterized by reddish scales.

The fish samples used in this experiment were obtained from Rameshwaram. On average, the Nagarai fish utilized in this study weighed 362.16 grams and measured 23.45 centimeters in length. Image acquisition was carried out using an iPhone 13 Pro Max mobile camera with a 12-megapixel resolution. Positioned vertically above the fish samples with a gap of 33 centimeters, the camera captured images with dimensions of 1568 x 1568 pixels. Throughout the experiment, the fish were preserved at a temperature of 0 degrees Celsius. Fresh samples were photographed after 24 hours, while non-fresh samples were captured after 3 days, enabling a comprehensive assessment of freshness levels. This experiment involved examining the quality of fish samples under varying conditions. Figure 2a illustrates a fresh fish sample image, while Figure 2b depicts a non-fresh fish sample.

### II. Determination of Fish Freshness Using Computer Vision
The proposed algorithm utilizes computer vision techniques to assess the freshness of fish, with a specific focus on analyzing the skin tissue. This tissue undergoes distinguishable changes that reflect the freshness of the fish. The algorithm begins by segmenting the skin region from the fish images using the saturation channel of the HSV transformed image. Following this segmentation, statistical features such as mean and variance are extracted from the segmented skin region to discern freshness levels over time. This process consists of three main steps:

1. **Segmentation of the Region of Interest (ROI)**
2. **Feature Extraction from the HSV Color Space of the ROI**
3. **Determination of the Freshness Range in the Fish**

#### 1. Segmentation of ROI
The proposed algorithm focuses on segmenting the region of interest (ROI), which is the skin of the fish. The algorithm is framed as follows:
1. RGB color image of the fish is loaded.
2. Input image is transformed from RGB to HSV.
3. Create a binary mask by defining the coordinates and dimensions of the rectangle. Set the pixel values within the rectangular region to 255. Pixels outside the rectangle remain zero.
4. Using the binary mask, the ROI segmentation is done from the saturation channel of HSV image.

#### 2. Feature Extraction
Extracting proper discriminatory features is a pivotal aspect of developing a framework for identifying the freshness level of fish samples. In this methodology, statistical features are derived from the segmented region within the saturation channel of the HSV color space. The saturation channel image encapsulates valuable insights into the skin color variations over time. The computed statistical parameters encompass the mean and variance. The mean signifies the average pixel intensity in a sample image and is computed as follows:
\[ \text{Mean} = \frac{1}{x \times y} \sum_{i=1}^{x} \sum_{j=1}^{y} I(i,j) \]
Where \( I(i,j) \) denotes the intensity value of the pixel at position \((i, j)\) in the ROI image of size \( x \times y \). The variance, on the other hand, quantifies the dispersion of intensity values among pixels in a sample image and is calculated as:
\[ \text{Variance} = \frac{1}{x \times y} \sum_{i=1}^{x} \sum_{j=1}^{y} (I(i,j) - \text{Mean})^2 \]
Figure 4 visually illustrates the degradation of both fresh and non-fresh fish skin.

#### 3. Freshness Detection
An identifiable pattern emerges from the analysis of statistical features extracted from the fish skin, which serves as the region of interest (ROI) in this study. Particularly, discernible variations are observed in the values of these statistical features within the saturation channel of the HSV color model. Building upon this observation, a framework is devised for detecting fish freshness, with a focus on extracting statistical features from the saturation channel. Tables 1 and 2 provide statistical data for 25 randomly selected samples from both fresh and non-fresh categories. The intensity of fish skin color naturally diminishes over time, resulting in a decline in the statistical feature values of non-fresh images, including mean and variance, in comparison to fresh ones. Leveraging this understanding, a freshness detection criterion is established. If both the mean and variance of the input sample fall below the calculated thresholds, the fish is classified as non-fresh; otherwise, it is classified as fresh.

## Experimental Results
To evaluate the developed framework, a total of 109 fish samples were utilized, comprising 59 fresh and 50 non-fresh samples. These samples were captured after 24 hours and 3 days, respectively, providing distinct categories for analysis. Of this dataset, 80 samples (43 fresh and 37 non-fresh) were allocated for training, while the remaining 29 samples (16 fresh and 13 non-fresh) were set aside for testing purposes. Statistical features, including mean and variance, were computed and analyzed as part of the evaluation process.

During testing, the framework correctly predicted 28 out of 29 samples, resulting in a high accuracy percentage of approximately 95.66%. The evaluation process involved the use of confusion matrices, with true positives represented as diagonal elements. Insights gained from variations in mean and variance values over time informed the design of a robust framework for freshness detection. Overall, the developed algorithm demonstrates efficiency and accuracy in discerning freshness ranges in post-harvested fish samples, showcasing its potential for application in aquaculture industries and consumer-oriented settings.

### Performance Metrics of the Proposed Method
The performance metrics used to evaluate the proposed method are as follows:
- **Accuracy**: 95.6%
- **Precision**: 100%
- **Recall**: 94.1%
- **F1-Score**: 96.9%

These metrics were calculated using a confusion matrix, which encapsulates the true positives, true negatives, false positives, and false negatives of the model's predictions.

## Conclusion
The proposed methodology presents an efficient and non-destructive approach to assess the freshness of fish. This method utilizes advanced image processing techniques to identify freshness indicators, with a particular focus on changes observed in the fish skin over time. By extracting statistical features from segmented skin tissue in the saturation channel of HSV transformed images, the framework achieves high accuracy in classifying the freshness of fish samples. The implementation of this methodology has significant implications for quality control in the fisheries industry, offering a reliable and cost-effective solution for ensuring fish freshness during post-harvest handling and storage. Future research may explore the integration of additional features and advanced machine learning techniques to further enhance the robustness and applicability of the framework across various fish species and environmental conditions.

## Note 
The codes provided in this project were experimented in Pycharm platform, if you want to run it in different platforms of python you have to modify some small changes accordingly (i,e. in my case I had to modify my code for running it in google colab). 
