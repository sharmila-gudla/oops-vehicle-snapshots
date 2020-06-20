from django.test import TestCase
from .utils import *
from freezegun import freeze_time
import pytest 
from .utils import * 





@pytest.fixture
def user():  # Our Fixture function
    user_obj = User.objects.create(name="sharmila",profile_pic="www.google.com")
    return user_obj
@pytest.fixture
def user2():  # Our Fixture function
    user2_obj = User.objects.create(name="srinu",profile_pic="www.facebook.com")
    return user2_obj

@pytest.fixture
def post(user):
    post_obj=Post.objects.create(content="happy birthday",posted_at=datetime.now(),posted_by_id=user.id)
    return post_obj
@pytest.fixture
def comment(user,post):
    comnt_obj=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id)
    return comnt_obj
@pytest.fixture
def reaction(user,comment):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    return react_obj
@pytest.fixture
def reaction2(user,post):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LIT",reacted_at=datetime.now())
    return react_obj

#create post

@pytest.mark.django_db
def test_create_post_user_id_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        create_post(1,"hiii how are you")


@pytest.mark.django_db
def test_create_post_content_raises_invalid_post_content_exception(user):
    with pytest.raises(InvalidPostContent):
        create_post(1,"")

@pytest.mark.django_db
def test_create_post_valid_user_id_and_post_content(user):
    post_1=create_post(1,"hello guys")
    check=Post.objects.get(id=1)
    assert post_1==check.id    
#create comment


@pytest.mark.django_db
def test_create_comment_user_id_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        create_comment(1,2,"hiii how are you")

@pytest.mark.django_db
def test_create_comment_post_id_raises_invalid_post_exception(user):
    with pytest.raises(InvalidPostException):
        create_comment(1,2,"hiii how are you")
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_create_comment_content_raises_invalid_comment_content_exception(user,post):
    with pytest.raises(InvalidCommentContent):
        create_comment(1,1,"")
#sharmila
@pytest.mark.django_db
def test_create_comment_valid_user_post_ids_and_comment_content(user2,post):
    comment_1=create_comment(user2.id,post.id,"Thank you")
    check=Comment.objects.get(id=1)
    assert comment_1==check.id    
#reply to comment

@pytest.mark.django_db
def test_reply_to_comment_user_id_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        reply_to_comment(2,2,"hiii how are you")

@pytest.mark.django_db
def test_reply_to_comment_comment_id_raises_invalid_comment_exception(user):
    with pytest.raises(InvalidCommentException):
        reply_to_comment(1,2,"hiii how are you")

@freeze_time(datetime.now())
@pytest.mark.django_db
def test_reply_to_comment_comment_content_raises_invalid_reply_content_exception(user2,post,user):
    Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user2.id,post_id=post.id)
    with pytest.raises(InvalidReplyContent):
        reply_to_comment(1,1,"")
#sharmila
@pytest.mark.django_db
def test_reply_to_comment_valid_user_comment_ids_and_reply_comment_without_parent_comment_id(user,post):
    comment=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id)
    comment_2=reply_to_comment(user.id,comment.id,reply_content="welcome")
    check=Comment.objects.get(id=2)
    assert comment_2==check.id
#sharmila
@pytest.mark.django_db
def test_reply_to_comment_valid_user_comment_ids_and_reply_comment_with_parent_comment_id(user,post,user2):
    comment=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id,parent_comment_id=user2.id)
    comment_2=reply_to_comment(user.id,comment.id,reply_content="welcome")
    check=Comment.objects.get(id=2)
    assert comment_2==check.id

#react to post

@pytest.mark.django_db
def test_react_to_post_user_id_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        react_to_post(1,2,"hiii how are you")

@pytest.mark.django_db
def test_react_to_post_post_id_raises_invalid_post_exception(user):
    with pytest.raises(InvalidPostException):
        react_to_post(1,2,"hiii how are you")
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_reaction_type_raises_invalid_reaction_type_exception_with_empty_field(user,post):
    with pytest.raises(InvalidReactionTypeException):
        react_to_post(1,1,"")
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_reaction_type_raises_invalid_reaction_type_exception_with_different_field(user,post):
    with pytest.raises(InvalidReactionTypeException):
        react_to_post(1,1,"HELLO")

@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_first_time(user,post):
    react_to_post(1,1,"LOVE")
    check=Reaction.objects.get(id=1)
    assert check.reaction=="LOVE"
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_second_time_already_existed_reaction(user,post):
    reaction_1=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LOVE",reacted_at=datetime.now())
    react_to_post(user.id,post.id,"LOVE")
    reaction_1=Reaction.objects.all()
    assert list(reaction_1)==[]
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_second_time_with_different_reaction(user,post):
    reaction_1=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LOVE",reacted_at=datetime.now())
    react_to_post(user.id,post.id,"WOW")
    reaction_1=Reaction.objects.all()
    assert reaction_1[0].reaction=="WOW"

#react to comment

@pytest.mark.django_db
def test_react_to_comment_user_id_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        react_to_comment(1,2,"hiii how are you")

@pytest.mark.django_db
def test_react_to_comment_post_id_raises_invalid_post_exception(user):
    with pytest.raises(InvalidCommentException):
        react_to_comment(1,2,"hiii how are you")
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_reaction_type_raises_invalid_reaction_type_exception_with_empty_field(user,comment):
    with pytest.raises(InvalidReactionTypeException):
        react_to_comment(1,1,"")
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_reaction_type_raises_invalid_reaction_type_exception_with_different_field(user,comment):
    with pytest.raises(InvalidReactionTypeException):
        react_to_comment(1,1,"HELLO")
  
    
#-------------
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_first_time(user,comment):
    react_to_comment(1,1,"LOVE")
    check=Reaction.objects.get(id=1)
    assert check.reaction=="LOVE"
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_second_time_already_existed_reaction(user,comment):
    reaction_1=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    react_to_comment(user.id,comment.id,"LOVE")
    reaction_1=Reaction.objects.all()
    assert list(reaction_1)==[]
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_second_time_with_different_reaction(user,comment):
    reaction_1=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    react_to_comment(user.id,comment.id,"WOW")
    reaction_1=Reaction.objects.all()
    assert reaction_1[0].reaction=="WOW"

@pytest.mark.django_db
def test_get_total_reaction_count_of_reactions_count(reaction,reaction2):
    a=get_total_reaction_count()
    assert a=={'count':2}

@pytest.mark.django_db
def test_get_reaction_metrics_for_given_post_id(post,reaction2):
    a=get_reaction_metrics(post_id=post.id)
    assert a=={'LIT':1}

@pytest.mark.django_db
def test_get_reaction_metrics_for_given_post_id_raises_invalid_exception(reaction2):
    with pytest.raises(InvalidPostException):
        get_reaction_metrics(6)

@pytest.mark.django_db
def test_delete_post_for_user_id_raises_invalid_user_exception(post):
    with pytest.raises(InvalidUserException):
        delete_post(7,post.id)

@pytest.mark.django_db
def test_delete_post_for_post_id_raises_invalid_post_exception(user):
    with pytest.raises(InvalidPostException):
        delete_post(user.id,5)

@pytest.mark.django_db
def delete_post_with_valid_user_post_ids(user,post):
    delete_post(user_id=user.id, post_id=post.id)
    a=Post.objects.filter(id=post.id,posted_by_id=user.id)
    assert list(a)==[]
  
@pytest.mark.django_db
def test_get_posts_with_more_positive_reactions_returns_post_ids(reaction2):
    a=get_posts_with_more_positive_reactions()
    assert list(a)==[1]

@pytest.mark.django_db
def test_get_posts_reacted_by_user_raises_invalid_user_exception():
    with pytest.raises(InvalidUserException):
        get_posts_reacted_by_user(user_id=1)

@pytest.mark.django_db
def test_get_posts_reacted_by_user_for_valid_details_of_user_id(user,reaction2):
    a=get_posts_reacted_by_user(user_id=user.id)
    assert list(a)==[1]

@pytest.mark.django_db
def test_get_reactions_to_post_raises_invalid_post_exception():
    with pytest.raises(InvalidPostException):
        get_reactions_to_post(post_id=3)
@pytest.mark.django_db
def test_get_reactions_to_post_for_valid_post_details(post):
    a=get_reactions_to_post(post_id=post.id)
    assert a==[]



  
'''   with pytest.raises(Exception) as e:
            assert RaceCar(color="Red",max_speed=40,acceleration=0,tyre_friction=3)
        assert str(e.value) == "Invalid value for acceleration"
'''