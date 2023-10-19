# Fantano Album Score Prediction Project

## Purpose

I love Anthony Fantano, *the internet's bussiest music nerd*. He reviews music on his Youtube channel, [The Needle Drop](https://www.youtube.com/channel/UCt7fwAhXDy3oNFTAzF2o8Pw). He also has a [website](https://www.theneedledrop.com/) where he lists his reviews. I wanted to see if I could predict his scores for albums based on the text of his reviews. I also wanted to build a web application where users could input their own reviews and get a predicted score, based on his reviews.

So far I have got the text from his reviews on YouTube, and I have extracted the scores from the descriptions of the videos. I have trained a Support Vector Machine (SVM) on this dataset and found out which single word terms are associated with high scoring albums:

![1697718900816](image/README/1697718900816.png)

This was fun, but ultimately not super surprising. What I think would be even more fun would be to expand my models (simple lasso model, fine-tuned BERT model with a regression head), emsemble these, and then make a web application where users can input their own reviews and get a predicted score. This would also be a good opportunity to learn about deploying models to an API and building a front-end application.

If I feel very inspired, I might automate it with GitHub actions so that it updates every month or so with new reviews.

## Context

Fantano reviews music. The majority of his reviews are albums. He has a [website](https://www.theneedledrop.com/) which lists his reviews. He has a [Youtube channel](https://www.youtube.com/channel/UCt7fwAhXDy3oNFTAzF2o8Pw) that he uploads his reviews on. See a sample below.

<iframe width="560" height="315" src="https://www.youtube.com/embed/TYE930nQfig?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Structure

### 1. Acquiring Data

- Set up a project on Google Cloud Platform.
- Enable the YouTube Data API and obtain an API key.
- Use the YouTube Data API to retrieve video transcripts and descriptions from Anthony Fantano's channel.
- Extract review scores from video descriptions.

### 2. Processing Raw Data

- Clean and preprocess the transcripts to remove any irrelevant information.
- Extract review text and associated scores.
- Store the processed data in a structured format (e.g., CSV or database).

### 3. Exploratory Data Analysis

- Load and explore the dataset to understand its characteristics.
- Perform basic statistics to find any patterns or trends in the data.
- Visualize the data to gain insights.

### 4. Building Models

#### 4.1 Lasso Regression Model

- Preprocess text data for modeling.
- Split the data into training and testing sets.
- Train a Lasso regression model on the training data.
- Evaluate the model's performance on the testing data.

#### 4.2 Support Vector Machine Model

- Train a SVM model on the training data.
- Evaluate the model's performance on the testing data.

#### 4.3 Fine-tuning a Pre-trained Model

- Load a pre-trained BERT model.
- Fine-tune the model on your dataset.
- Evaluate the model's performance.

#### 4.4 Ensemble Model

- Combine the predictions from the Lasso model, SVM model, and fine-tuned BERT model.
- Evaluate the ensemble model's performance.

### 5. Testing

- Test the ensemble model on a separate test set to validate its performance.
- Make any necessary adjustments to the models or ensemble method based on test results.

### 6. Deploying to an API

- Save the trained ensemble model.
- Set up a web server with an API endpoint to handle review scoring requests.
- Load the trained ensemble model in the server and handle incoming requests.

### 7. Front-End Development

- Set up a SvelteKit project for the front-end application.
- Create a review form where users can input their reviews.
- Implement functionality to send the review to the API endpoint and display the predicted score.

### 8. Deployment

- Deploy the front-end application to a web server or cloud platform.
- Ensure that the API endpoint is accessible from the front-end application.
- Test the end-to-end functionality of the application.

### 9. Maintenance

- Monitor the application for any issues or errors.
- Make updates as necessary based on user feedback or changes to the YouTube Data API.
