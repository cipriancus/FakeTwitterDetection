package twitter.nlp.service.impl;

import twitter.nlp.entity.Sentiment;
import twitter.nlp.service.ISentiment;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import twitter.exception.InvalidInputException;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.Properties;

@Component
public class SentimentAnalysis implements ISentiment {

    private RestTemplate restTemplate;
    private String requestString = "http://www.sentiment140.com/api/classify?";
    private Properties sentimentProp;

    public SentimentAnalysis() {
        sentimentProp = new Properties();
        restTemplate = new RestTemplate();
        try {
            sentimentProp.load(getClass().getClassLoader().getResourceAsStream("sentiment.properties"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String constructRequestString(String textToClasify) {
        try {
            requestString = requestString + "text=" + URLEncoder.encode(textToClasify, "UTF-8") + "&" + "appid=" + sentimentProp.getProperty("appid") + "&" + "language=" + "auto";
            System.out.println(requestString);
            return requestString;
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return "";
        }
    }

    public int calculateSentiment(String text) throws InvalidInputException {
        if (text == null || text.length() == 0)
            throw new InvalidInputException();

        String url = constructRequestString(text);

        Sentiment sentiment = restTemplate.getForObject(url, Sentiment.class);

        if (sentiment != null) {
            System.out.print(sentiment.results.polarity);
            return sentiment.results.polarity;
        }
        return -1;
    }
}