package twitter.nlp.util;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan(basePackages = {"nlp.service,nlp.service.impl,nlp.aspect"})
public class App {
}