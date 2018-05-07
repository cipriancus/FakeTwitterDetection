package twitter.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import twitter.entity.Tweet;
import twitter.repository.TweetRepository;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(propagation = Propagation.REQUIRES_NEW)
public class TweetService {
    @Autowired
    private TweetRepository tweetRepository;

    public Tweet save(Tweet tweet) {
        return tweetRepository.save(tweet);
    }

    public List<Tweet> findAll() {
        return tweetRepository.findAll();
    }

    public long countRecords() {
        return tweetRepository.count();
    }

    public List<Tweet> getByPage(int page, int noOfItems) {
        return tweetRepository.findAll(new PageRequest(page, noOfItems)).getContent();
    }
}
