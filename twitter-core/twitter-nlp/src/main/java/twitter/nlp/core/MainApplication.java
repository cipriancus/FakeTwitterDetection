package twitter.nlp.core;

import twitter.nlp.service.IParseFacade;
import twitter.nlp.service.ISentiment;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApplication {
    public static void main(String[] args) throws Exception {

        ApplicationContext appContext = new ClassPathXmlApplicationContext("classpath:META-INF/twitter/nlp/applicationContext.xml");
        String text = "is a beautiful day";
        ISentiment sent = (ISentiment) appContext.getBean("senti");
        System.out.println("the sentiment is" + sent.calculateSentiment(text));
        IParseFacade parse = (IParseFacade) appContext.getBean("lemmat");
        System.out.println("the lemmatization is" + parse.getResult(text));
        IParseFacade parseTok = (IParseFacade) appContext.getBean("token");
        System.out.println("the token is" + parseTok.getResult(text));

    }
}
