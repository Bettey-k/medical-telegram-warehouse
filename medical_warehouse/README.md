## Task 3 – Analysis of Image Content Patterns

### Do promotional posts get more views than product_display posts?
Based on the YOLO object detection results integrated into the data warehouse,
posts categorized as **promotional** (images containing both people and products)
generally show higher average view counts than **product_display** posts.
This suggests that human presence in images increases engagement and visibility.

### Which channels use more visual content?
Channels focused on cosmetics and consumer medical products tend to use images
more frequently than pharmaceutical information channels. These channels also
show a higher proportion of promotional and lifestyle image categories, indicating
a stronger emphasis on visual marketing strategies.

### Limitations of using pre-trained object detection models
YOLOv8 is a general-purpose object detection model and is not trained to recognize
domain-specific medical products. As a result, it detects generic objects
(e.g., bottles, persons) rather than specific medicines or brands.
This limits fine-grained classification accuracy and may lead to misclassification.
Custom-trained models or domain-specific datasets would improve precision.
