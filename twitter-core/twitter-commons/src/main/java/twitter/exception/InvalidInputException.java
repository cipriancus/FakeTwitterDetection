package twitter.exception;

public class InvalidInputException extends Exception {
    public InvalidInputException(){
        super("Invalid input provided");
    }
}
