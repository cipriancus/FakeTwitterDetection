package twitter.repository;


import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.CrudRepository;
import twitter.entity.Tweet;

public interface TweetRepository extends AbstractSocialNetworkRepository<Tweet> {
    Page<Tweet> findAll(Pageable page);
}
