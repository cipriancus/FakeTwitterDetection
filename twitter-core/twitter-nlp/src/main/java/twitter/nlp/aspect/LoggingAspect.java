package twitter.nlp.aspect;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;

import java.util.Arrays;

@Aspect
public class LoggingAspect {

    @Before("execution(* twitter.nlp.service.ISentiment.calculateSentiment(..))")
    public void logBefore(JoinPoint joinPoint) {

        System.out.println("logBefore() is running!");
        System.out.println("the method is : " + joinPoint.getSignature().getName());
        System.out.println("******");
    }

    @After("execution(* twitter.nlp.service.IParseFacade.getResult(..))")
    public void logAfter(JoinPoint joinPoint) {

        System.out.println("logAfter() is running!");
        System.out.println("the method is : " + joinPoint.getSignature().getName());
        System.out.println("******");

    }

    @AfterReturning(pointcut = "execution(* twitter.nlp.service.impl.Tokenizer.getResult(..))", returning = "result")
    public void logAfterReturning(JoinPoint joinPoint, Object result) {

        System.out.println("logAfterReturning() is running!");
        System.out.println("method is : " + joinPoint.getSignature().getName());
        System.out.println("Method returned value is : " + result);
        System.out.println("******");

    }

    @Around("execution(* twitter.nlp.service.impl.Lemmatize.getResult(..))")
    public void logAround(ProceedingJoinPoint joinPoint) throws Throwable {

        System.out.println("logAround() is running!");
        System.out.println(" method : " + joinPoint.getSignature().getName());
        System.out.println("method has following arguments : " + Arrays.toString(joinPoint.getArgs()));

        System.out.println("Around before is running!");
        joinPoint.proceed();
        System.out.println("Around after is running!");

        System.out.println("******");

    }

}