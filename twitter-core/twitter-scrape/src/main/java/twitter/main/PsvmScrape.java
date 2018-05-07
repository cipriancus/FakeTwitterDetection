package twitter.main;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Component;
import twitter.exception.InvalidInputException;
import twitter.scrape.TwitterScrape;
import javax.annotation.PostConstruct;

public class PsvmScrape {
    @Autowired
    private TwitterScrape twitterScrape;

    private static TwitterScrape SCRAPING_CONTROLLER;

    public static void main(String[] args) {
        //"classpath:META-INF/twitter/spark/applicationContext.xml"
        new ClassPathXmlApplicationContext("classpath:META-INF/twitter/applicationContext.xml", "classpath:META-INF/twitter/scrape/applicationContext.xml");
        try {
            SCRAPING_CONTROLLER.scrape("#obama");
        }catch (InvalidInputException e){
            e.printStackTrace();
        }
    }

    @PostConstruct
    void init() {
        if (twitterScrape == null)
            System.out.println("NULLL");
        SCRAPING_CONTROLLER = twitterScrape;
    }
}