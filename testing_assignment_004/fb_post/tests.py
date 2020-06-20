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
def post2(user2):
    post2_obj=Post.objects.create(content="happy birthday to you",posted_at=datetime.now(),posted_by_id=user2.id)
    return post2_obj

@pytest.fixture
def comment(user,post):
    comnt_obj=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id)
    return comnt_obj
@pytest.fixture
def comment2(user2,post2,comment):
    comnt2_obj=Comment.objects.create(content="we welcomes you",commented_at=datetime.now(),commented_by_id=user2.id,post_id=post2.id,parent_comment_id=comment2.id)
    return comnt2_obj

@pytest.fixture
def reaction(user,comment):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    return react_obj
@pytest.fixture
def reaction2(user,post):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LIT",reacted_at=datetime.now())
    return react_obj
@pytest.fixture
def reaction3(user,post):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="THUMBS-DOWN",reacted_at=datetime.now())
    return react_obj
@pytest.fixture
def reaction4(user,post2):
    react_obj=Reaction.objects.create(reacted_by_id=user.id,post_id=post2.id,reaction="LIT",reacted_at=datetime.now())
    return react_obj

#create post

@pytest.mark.django_db
def test_create_post_user_id_raises_invalid_user_exception():
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidUserException):
        create_post(id_one,"hiii how are you")
    #Assert

@pytest.mark.django_db
def test_create_post_content_raises_invalid_post_content_exception(user):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidPostContent):
        create_post(id_one,"")
    #Assert

@pytest.mark.django_db
def test_create_post_valid_user_id_and_post_content(user):
    #Arrange
    id_one=1
    #Act
    post_1=create_post(id_one,"hello guys")
    #Assert
    check=Post.objects.get(id=id_one)
    assert post_1==check.id    
#create comment


@pytest.mark.django_db
def test_create_comment_user_id_raises_invalid_user_exception():
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidUserException):
        create_comment(id_one,id_two,"hiii how are you")
    #Assert

@pytest.mark.django_db
def test_create_comment_post_id_raises_invalid_post_exception(user):
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidPostException):
        create_comment(id_one,id_two,"hiii how are you")
    #Assert
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_create_comment_content_raises_invalid_comment_content_exception(user,post):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidCommentContent):
        create_comment(id_one,id_one,"")
    #Assert

@pytest.mark.django_db
def test_create_comment_valid_user_post_ids_and_comment_content(user2,post):
    #Arrange
    id_one=1
    #Act
    comment_1=create_comment(user2.id,post.id,"Thank you")
    #Assert
    check=Comment.objects.get(id=id_one)
    assert comment_1==check.id    
#reply to comment

@pytest.mark.django_db
def test_reply_to_comment_user_id_raises_invalid_user_exception():
    #Arrange
    id_two=2
    #Act
    with pytest.raises(InvalidUserException):
        reply_to_comment(id_two,id_two,"hiii how are you")
    #Assert

@pytest.mark.django_db
def test_reply_to_comment_comment_id_raises_invalid_comment_exception(user):
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidCommentException):
        reply_to_comment(id_one,id_two,"hiii how are you")
    #Assert

@freeze_time(datetime.now())
@pytest.mark.django_db
def test_reply_to_comment_comment_content_raises_invalid_reply_content_exception(user2,post,user):
    #Arrange
    id_one=1
    Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user2.id,post_id=post.id)
    #Act
    with pytest.raises(InvalidReplyContent):
        reply_to_comment(id_one,id_one,"")
    #Assert

@pytest.mark.django_db
def test_reply_to_comment_valid_user_comment_ids_and_reply_comment_without_parent_comment_id(user,post):
    #Arrange
    id_two=2
    comment=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id)
    #Act
    comment_2=reply_to_comment(user.id,comment.id,reply_content="welcome")
    #Assert
    check=Comment.objects.get(id=id_two)
    assert comment_2==check.id

@pytest.mark.django_db
def test_reply_to_comment_valid_user_comment_ids_and_reply_comment_with_parent_comment_id(user,post,user2):
    #Arrange
    id_two=2
    comment=Comment.objects.create(content="welcome",commented_at=datetime.now(),commented_by_id=user.id,post_id=post.id,parent_comment_id=user2.id)
    #Act
    comment_2=reply_to_comment(user.id,comment.id,reply_content="welcome")
    #Assert
    check=Comment.objects.get(id=id_two)
    assert comment_2==check.id

#react to post

@pytest.mark.django_db
def test_react_to_post_user_id_raises_invalid_user_exception():
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidUserException):
        react_to_post(id_one,id_two,"hiii how are you")
    #Assert

@pytest.mark.django_db
def test_react_to_post_post_id_raises_invalid_post_exception(user):
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidPostException):
        react_to_post(id_one,id_two,"hiii how are you")
    #Assert
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_reaction_type_raises_invalid_reaction_type_exception_with_empty_field(user,post):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidReactionTypeException):
        react_to_post(id_one,id_one,"")
    #Assert
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_reaction_type_raises_invalid_reaction_type_exception_with_different_field(user,post):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidReactionTypeException):
        react_to_post(id_one,id_one,"HELLO")
    #Assert

@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_first_time(user,post):
    #Arrange
    id_one=1
    #Act
    react_to_post(id_one,id_one,"LOVE")
    #Assert
    check=Reaction.objects.get(id=id_one)
    assert check.reaction=="LOVE"
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_second_time_already_existed_reaction(user,post,reaction2):
    #reaction_1=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LOVE",reacted_at=datetime.now())
    #Arrange
    #Act
    react_to_post(user.id,post.id,"LIT")
    #Assert
    reaction_1=Reaction.objects.all()
    assert list(reaction_1)==[]
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_post_valid_reaction_type_for_the_second_time_with_different_reaction(user,post,reaction2):
    #reaction_1=Reaction.objects.create(reacted_by_id=user.id,post_id=post.id,reaction="LOVE",reacted_at=datetime.now())
    #Arrange
    
    #Act
    react_to_post(user.id,post.id,"WOW")
    #Assert
    reaction_1=Reaction.objects.all()
    assert reaction_1[0].reaction=="WOW"

#react to comment

@pytest.mark.django_db
def test_react_to_comment_user_id_raises_invalid_user_exception():
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidUserException):
        react_to_comment(id_one,id_two,"hiii how are you")
    #Assert

@pytest.mark.django_db
def test_react_to_comment_post_id_raises_invalid_post_exception(user):
    #Arrange
    id_one=1
    id_two=2
    #Act
    with pytest.raises(InvalidCommentException):
        react_to_comment(id_one,id_two,"hiii how are you")
    #Assert
    
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_reaction_type_raises_invalid_reaction_type_exception_with_empty_field(user,comment):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidReactionTypeException):
        react_to_comment(id_one,id_one,"")
    #Assert
    
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_reaction_type_raises_invalid_reaction_type_exception_with_different_field(user,comment):
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidReactionTypeException):
        react_to_comment(id_one,id_one,"HELLO")
    #Assert
  
    
#-------------
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_first_time(user,comment):
    #Arrange
    id_one=1
    #Act
    react_to_comment(id_one,id_one,"LOVE")
    #Assert
    check=Reaction.objects.get(id=id_one)
    assert check.reaction=="LOVE"
    
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_second_time_already_existed_reaction(user,comment,reaction):
    #reaction_1=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    #Arrange
    #Act
    react_to_comment(user.id,comment.id,"LOVE")
    #Assert
    reaction_1=Reaction.objects.all()
    assert list(reaction_1)==[]
@freeze_time(datetime.now())
@pytest.mark.django_db
def test_react_to_comment_valid_reaction_type_for_the_second_time_with_different_reaction(user,comment,reaction):
    #reaction_1=Reaction.objects.create(reacted_by_id=user.id,comment_id=comment.id,reaction="LOVE",reacted_at=datetime.now())
    #Arrange
    
    #Act
    react_to_comment(user.id,comment.id,"WOW")
    #Assert
    reaction_1=Reaction.objects.all()
    assert reaction_1[0].reaction=="WOW"

@pytest.mark.django_db
def test_get_total_reaction_count_of_reactions_count(reaction,reaction2):
    #Arrange
    
    #Act
    a=get_total_reaction_count()
    #Assert
    assert a=={'count':2}

@pytest.mark.django_db
def test_get_reaction_metrics_for_given_post_id(post,reaction2):
    #Arrange
    
    #Act
    a=get_reaction_metrics(post_id=post.id)
    #Assert
    assert a=={'LIT':1}
@pytest.mark.django_db
def test_get_reaction_metrics_for_given_post_id_more_than_one(post,reaction2,reaction3):
     #Arrange
    
    #Act
    a=get_reaction_metrics(post_id=post.id)
    #Assert
    assert a=={'LIT':1,"THUMBS-DOWN":1}

@pytest.mark.django_db
def test_get_reaction_metrics_for_given_post_id_raises_invalid_exception(reaction2):
    #Arrange
    id_six=6
    #Act
    with pytest.raises(InvalidPostException):
        get_reaction_metrics(id_six)
    #Assert

@pytest.mark.django_db
def test_delete_post_for_user_id_raises_invalid_user_exception(post):
    #Arrange
    id_seven=7
    #Act
    with pytest.raises(InvalidUserException):
        delete_post(id_seven,post.id)
    #Assert
    
@pytest.mark.django_db
def test_delete_post_for_post_id_raises_invalid_post_exception(user):
    #Arrange
    id_five=5
    #Act
    with pytest.raises(InvalidPostException):
        delete_post(user.id,id_five)
    #Assert
    
@pytest.mark.django_db
def test_delete_post_for_post_id_not_equal_to_user_id_raises_cannot_delete_post_exception(user,post2):
    #Arrange
    
    #Act
    with pytest.raises(UserCannotDeletePostException):
        delete_post(user.id,post2.id)
    #Assert


@pytest.mark.django_db
def delete_post_with_valid_user_post_ids(user,post):
    #Arrange
    #Act
    delete_post(user_id=user.id, post_id=post.id)
    #Assert
    a=Post.objects.filter(id=post.id,posted_by_id=user.id)
    assert list(a)==[]
  
@pytest.mark.django_db
def test_get_posts_with_more_positive_reactions_returns_post_ids(reaction2):
    #Arrange
    id_one=1
    #Act
    a=get_posts_with_more_positive_reactions()
    #Assert
    assert list(a)==[id_one]
@pytest.mark.django_db
def test_get_posts_with_negative_reactions_returns_empty_list(reaction3):
    #Arrange
    
    #Act
    a=get_posts_with_more_positive_reactions()
    #Assert
    assert list(a)==[]
'''
@pytest.mark.django_db
def test_get_posts_with_equal_positive_and_negative_reactions_returns_empty_list(user,post,post2,reaction3,reaction4):
    #Arrange
    
    #Act
    a=get_posts_with_more_positive_reactions()
    #Assert
    assert list(a)==[]
'''   
@pytest.mark.django_db
def test_get_posts_reacted_by_user_raises_invalid_user_exception():
    #Arrange
    id_one=1
    #Act
    with pytest.raises(InvalidUserException):
        get_posts_reacted_by_user(user_id=id_one)
    #Assert

@pytest.mark.django_db
def test_get_posts_reacted_by_user_for_valid_details_of_user_id(user,reaction2):
    #Arrange
    id_one=1
    #Act
    a=get_posts_reacted_by_user(user_id=user.id)
    #Assert
    assert list(a)==[id_one]

@pytest.mark.django_db
def test_get_reactions_to_post_raises_invalid_post_exception():
    #Arrange
    id_three=3
    #Act
    with pytest.raises(InvalidPostException):
        get_reactions_to_post(post_id=id_three)
    #Assert
@pytest.mark.django_db
def test_get_reactions_to_post_for_valid_post_details(post,reaction2):
    #Arrange
    
    #Act
    a=get_reactions_to_post(post_id=post.id)
    #Assert
    assert list(a)==[{'user_id':1,'name':'sharmila','profile_pic':'www.google.com','reaction':'LIT'}]
#task 13
@pytest.mark.django_db
def test_get_post_raises_invalid_post_exception():
    #Arrange
    id_three=3
    #Act
    with pytest.raises(InvalidPostException):
        get_post(post_id=id_three)
    #Assert
@freeze_time(str(datetime.now()))
@pytest.mark.django_db
def test_get_post_with_no_comments_return_empty_list(user):
    #Arrange
    id_one=1
    create_post(id_one,"happy birthday")
    #Act
    a=get_post(id_one)
    #Assert
    assert a=={'post_id': 1, 
                'posted_by': {
                    'name': 'sharmila', 
                    'user_id': 1, 
                    'profile_pic': 'www.google.com'
                    
                }, 
                'posted_at': str(datetime.now()), 
                'post_content': 'happy birthday', 
                'reactions': {
                    'count': 0,
                    'type': []
                    
                }, 
                'comments': [],
                'comments_count': 0
        
    }
@freeze_time(str(datetime.now()))
@pytest.mark.django_db
def test_get_post_with_no_replies_return_empty_list():
    #Arrange
    d=User.objects.create(name="srinu",profile_pic="www.facebook.com")
    c=create_post(d.id,"happy birthday")
    b=create_comment(d.id,c,"happy day")
    #Act
    a=get_post(c)
    #Assert
    assert a=={'post_id': 1, 
         'posted_by': {
         'name': 'srinu',
         'user_id': 1, 
         'profile_pic': 'www.facebook.com'},
         'posted_at': str(datetime.now()), 
         'post_content': 'happy birthday',
         'reactions': {
         'count': 0, 
         'type': []},
         'comments': [{
         'comment_id': 1, 
         'commenter': {
         'user_id': 1, 
         'name': 'srinu',
         'profile_pic': 'www.facebook.com'},
         'commented_at': str(datetime.now()), 
         'comment_content': 'happy day', 
         'reactions':
         {'count': 0, 
         'type': []},
         'replies_count': 0, 
         'replies': []}],
         'comments_count': 1}
@freeze_time(str(datetime.now()))
@pytest.mark.django_db
def test_get_post_with_valid_details_return_dictionary():
    #Arrange
    d=User.objects.create(name="srinu",profile_pic="www.facebook.com")
    c=create_post(d.id,"happy birthday")
    b=create_comment(d.id,c,"happy day")
    e=reply_to_comment(d.id,b, "thanks for ur wishes")
    react_to_post(d.id, c, "LOVE")
    react_to_comment(d.id, b, "WOW")
    #Act
    a=get_post(c)
    #Assert
    assert a=={'post_id': 1,
'posted_by': {
'name': 'srinu',
'user_id': 1,
'profile_pic': 'www.facebook.com'},
'posted_at': str(datetime.now()), 
'post_content': 'happy birthday',
'reactions': {
'count': 1, 
'type': ['LOVE']}, 
'comments': [{
'comment_id': 1, 
'commenter': {
'user_id': 1,
'name': 'srinu', 
'profile_pic': 'www.facebook.com'}, 
'commented_at': str(datetime.now()),
'comment_content': 'happy day', 
'reactions': {'count': 1,
'type': ['WOW']}, 
'replies_count': 1,
'replies': [{'comment_id': 2, 
'commenter': {'user_id': 1,
'name': 'srinu',
'profile_pic': 'www.facebook.com'}, 
'commented_at': str(datetime.now()), 
'comment_content': 'thanks for ur wishes',
'reactions': {'count': 0, 'type': []}}]}], 'comments_count': 1}
#tcde fg
@pytest.mark.django_db
def test_get_user_posts_for_user_id_raises_invalid_user_exception():
    #Arrange
    id_seven=7
    #Act
    with pytest.raises(InvalidUserException):
        get_user_posts(id_seven)
    #Assert
@freeze_time(str(datetime.now()))
@pytest.mark.django_db
def test_get_user_posts_with_valid_details_return_list_of_post_ids():
    #Arrange
    d=User.objects.create(name="srinu",profile_pic="www.facebook.com")
    c=create_post(d.id,"happy birthday")
    b=create_comment(d.id,c,"happy day")
    e=reply_to_comment(d.id,b, "thanks for ur wishes")
    react_to_post(d.id, c, "LOVE")
    react_to_comment(d.id, b, "WOW")
    #Act
    a=get_user_posts(d.id)
    #Assert
    assert list(a)==[{'post_id': 1,
'posted_by': {
'name': 'srinu',
'user_id': 1,
'profile_pic': 'www.facebook.com'},
'posted_at': str(datetime.now()), 
'post_content': 'happy birthday',
'reactions': {
'count': 1, 
'type': ['LOVE']}, 
'comments': [{
'comment_id': 1, 
'commenter': {
'user_id': 1,
'name': 'srinu', 
'profile_pic': 'www.facebook.com'}, 
'commented_at': str(datetime.now()),
'comment_content': 'happy day', 
'reactions': {'count': 1,
'type': ['WOW']}, 
'replies_count': 1,
'replies': [{'comment_id': 2, 
'commenter': {'user_id': 1,
'name': 'srinu',
'profile_pic': 'www.facebook.com'}, 
'commented_at': str(datetime.now()), 
'comment_content': 'thanks for ur wishes',
'reactions': {'count': 0, 'type': []}}]}], 'comments_count': 1}]

#task 15
@pytest.mark.django_db
def test_get_replies_for_comment_comment_id_raises_invalid_comment_exception():
    #Arrange
    id_six=6
    #Act
    with pytest.raises(InvalidCommentException):
        get_replies_for_comment(id_six)
    #Assert
@freeze_time(str(datetime.now()))
@pytest.mark.django_db
def test_get_replies_for_comment_with_valid_details_return_comment_and_user():
    #Arrange
    d=User.objects.create(name="srinu",profile_pic="www.facebook.com")
    c=create_post(d.id,"happy birthday")
    b=create_comment(d.id,c,"happy day")
    #Act
    e=reply_to_comment(d.id,b, "Thanks for ur wishes")
    #Assert
    assert get_replies_for_comment(b)== [{
                                        "comment_id": 2,
                                        "commenter": {
                                                    "user_id": 1,
                                                    "name": "srinu",
                                                    "profile_pic": "www.facebook.com"
                                                     },
                                        "commented_at": str(datetime.now()),
                                        "comment_content": "Thanks for ur wishes",
                                         }]

    