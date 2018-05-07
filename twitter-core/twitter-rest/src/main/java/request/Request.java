package request;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.social.twitter.api.Tweet;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

public class Request {

    private RestTemplate restTemplate = new RestTemplate();

    private String requestURL = "http://127.0.0.1:5000/classification";

    public String classify(Tweet tweet) {
        MultiValueMap<String, String> allArguments= new LinkedMultiValueMap<>();

        allArguments.add("Date", tweet.getCreatedAt().toString());
        allArguments.add("Tweet_Text", tweet.getText());
        allArguments.add("Tweet_Id", tweet.getIdStr());
        allArguments.add("User_Id", Long.toString(tweet.getFromUserId()));
        allArguments.add("User_Name", tweet.getUser().getName());
        allArguments.add("User_Screen_Name", tweet.getUser().getScreenName());
        allArguments.add("Retweets", Integer.toString(tweet.getRetweetCount()));
        allArguments.add("Favorites", Integer.toString(tweet.getFavoriteCount()));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(allArguments, headers);

        ResponseEntity<String> response = restTemplate.postForEntity( requestURL, request , String.class );

        return response.getBody();
    }

    public String classifyTweetEntity(twitter.entity.Tweet tweet) {
        MultiValueMap<String, String> allArguments= new LinkedMultiValueMap<>();

        allArguments.add("Date", tweet.getCreatedAt().toString());
        allArguments.add("Tweet_Text", tweet.getText());
        allArguments.add("Tweet_Id", tweet.getIdStr());
        allArguments.add("User_Id", Long.toString(tweet.getFromUserId()));
        allArguments.add("User_Name", tweet.getUserName());
        allArguments.add("User_Screen_Name", tweet.getScreenName());
        allArguments.add("Retweets", Integer.toString(tweet.getRetweetCount()));
        allArguments.add("Favorites", Integer.toString(tweet.getFavoriteCount()));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(allArguments, headers);

        ResponseEntity<String> response = restTemplate.postForEntity( requestURL, request , String.class );

        return response.getBody();
    }
}