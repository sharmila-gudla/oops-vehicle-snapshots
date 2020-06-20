from .models import *
from .exceptions import *
from django.db.models import *

from django.db import *

from datetime import datetime
#task 2
def create_post(user_id, post_content):
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    if not post_content:
        raise InvalidPostContent
        
    new_post=Post.objects.create(content=post_content,posted_by_id=user_id,posted_at=datetime.now())
    return new_post.id
#task 3
def create_comment(user_id, post_id, comment_content):
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    if not Post.objects.filter(id=post_id).exists():
        raise InvalidPostException
    if not comment_content:
        raise InvalidCommentContent
    new_comment=Comment.objects.create(content=comment_content,
                                       commented_by_id=user_id,
                                       post_id=post_id,
                                       commented_at=datetime.now()
                                       )
    return new_comment.id

#task 4
def reply_to_comment(user_id, comment_id, reply_content):
    comment=Comment.objects.filter(id=comment_id)
    user=User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    if not comment:
        raise InvalidCommentException
    if not reply_content:
        raise InvalidReplyContent
    if comment[0].parent_comment_id:
        reply_comment=Comment.objects.create(content=reply_content,
                                         commented_by_id=user_id,
                                        commented_at=datetime.now(),
                                        post_id=comment[0].post_id,
                                        parent_comment_id=comment[0].parent_comment_id) 
    else:
        
        reply_comment=Comment.objects.create(content=reply_content,
                                         commented_by_id=user_id,
                                        commented_at=datetime.now(),
                                        post_id=comment[0].post_id,
                                        parent_comment_id=comment_id)  
    return reply_comment.id
#task 5
def react_to_post(user_id, post_id, reaction_type):
    user_1=User.objects.filter(id=user_id)
    post_1=Post.objects.filter(id=post_id)
    reaction_2=Reaction.objects.filter(reacted_by_id=user_id, post_id =post_id)
    if not user_1:
        raise InvalidUserException
    if not post_1:
        raise InvalidPostException
    if reaction_type not in["WOW","LOVE","LIT","THUMBS-UP","THUMBS-DOWN","SAD","ANGRY","HAHA"]:
        raise InvalidReactionTypeException
    if not reaction_2:
        Reaction.objects.create(post_id=post_id,reaction=reaction_type,reacted_by_id=user_id,reacted_at=datetime.now())
    else:
        if reaction_2[0].reaction==reaction_type:
            reaction_2[0].delete()
        else:
            reaction_1=reaction_2[0]
            reaction_1.reaction=reaction_type
            reaction_1.reacted_at=datetime.now()
            reaction_1.save()
            
            
#task 6
def react_to_comment(user_id, comment_id, reaction_type):
    user_1=User.objects.filter(id=user_id)
    comment_1=Comment.objects.filter(id=comment_id)
    reaction_2=Reaction.objects.filter(reacted_by_id=user_id, comment_id =comment_id)
    if not user_1:
        raise InvalidUserException
    if not comment_1:
        raise InvalidCommentException
    if reaction_type not in["WOW","LOVE","LIT","THUMBS-UP","THUMBS-DOWN","SAD","ANGRY","HAHA"]:
        raise InvalidReactionTypeException
    if not reaction_2:
        Reaction.objects.create(comment_id=comment_id,reaction=reaction_type,reacted_by_id=user_id,reacted_at=datetime.now())
    else:
        if reaction_2[0].reaction==reaction_type:
            reaction_2[0].delete()
        else:
            reaction_1=reaction_2[0]
            reaction_1.reaction=reaction_type
            reaction_1.reacted_at=datetime.now()
            reaction_1.save()
#task 7
def get_total_reaction_count():
    return Reaction.objects.aggregate(count=Count("reaction"))
    #return Post.objects.aggregate(count=Count("post_reaction__reaction"))
#task 8
def get_reaction_metrics(post_id):
    post_1=Post.objects.filter(id=post_id)
    if not post_1:
        raise InvalidPostException   
    a=Reaction.objects.filter(post_id=post_id).values_list("reaction").annotate(Count("reaction"))
    return dict(a)
#task 9
def delete_post(user_id, post_id):
    user_1=User.objects.filter(id=user_id)
    post_1=Post.objects.filter(id=post_id)
      
    if not post_1:
        raise InvalidPostException    
    if post_1[0].posted_by_id==user_id:
        post_1[0].delete()
    
    if not user_1:
        raise InvalidUserException
    if post_1[0].posted_by_id!=user_id:
        raise UserCannotDeletePostException
    
#task 10
def get_posts_with_more_positive_reactions():
    positive=["THUMBS-UP","LIT","LOVE","HAHA","WOW"]  
    negative=["SAD","ANGRY","THUMBS-DOWN"] 
    pos=Count('reaction',filter=Q(reaction__in=positive))  
    neg=Count("reaction",filter=Q(reaction__in=negative))
    total=Reaction.objects.annotate(pos=pos).annotate(neg=neg).filter(pos__gt=F('neg')).values_list("post_id",flat=True).distinct()
    return total
    

#task 11
def get_posts_reacted_by_user(user_id):
    user_1=User.objects.filter(id=user_id)
    if not user_1:
        raise InvalidUserException
    reaction_1=Reaction.objects.filter(reacted_by=user_id)  
    post_list=[]
    for i in reaction_1: 
         item=i.post_id 
         post_list.append(item)
    return post_list
          
#task 12
def get_reactions_to_post(post_id):
    post_1=Post.objects.filter(id=post_id)
    if not post_1:
        raise InvalidPostException
    reactions_of_post=Reaction.objects.filter(post_id=post_id)
    post_list=[]
    user_dict={}
    for i in reactions_of_post:
        user_dict["user_id"]=i.reacted_by_id
        user_dict["name"]=i.reacted_by.name
        user_dict["profile_pic"]=i.reacted_by.profile_pic
        user_dict["reaction"]=i.reaction
        post_list.append(user_dict)
        user_dict={}
    return post_list

#task 13
def get_dict(post):
    comment_list = []
    for comment in list(post.comments.all()):
        reply_list=[]
        for reply in list(post.comments.all()):
            if reply.parent_comment_id == comment.id:
                replies ={
                    "comment_id": reply.id,
                    "commenter": {
                    "user_id": reply.commented_by_id,
                    "name": reply.commented_by.name,
                    "profile_pic": reply.commented_by.profile_pic
                },
                "commented_at": str(reply.commented_at)[:-6],
                "comment_content": reply.content,
                "reactions": {
                    "count": reply.reaction.count(),
                    "type": list(dict.fromkeys([p.reaction for p in reply.reaction.all()]))
                    }
                }
                reply_list.append(replies)
        if not comment.parent_comment_id:
            comment = {
                "comment_id": comment.id,
                "commenter": {
                    "user_id": comment.commented_by_id,
                    "name": comment.commented_by.name,
                    "profile_pic": comment.commented_by.profile_pic
                },
                "commented_at": str(comment.commented_at)[:-6],
                "comment_content": comment.content,
                "reactions": {
                    "count": comment.reaction.count(),
                    "type": list(dict.fromkeys([p.reaction for p in comment.reaction.all()]))
                },
                "replies_count": len(reply_list),
                "replies": reply_list,
            }
            comment_list.append(comment)

    res = {
        "post_id": post.id,
        "posted_by": {
            "name": post.posted_by.name,
            "user_id": post.posted_by_id,
            "profile_pic": post.posted_by.profile_pic
        },
        "posted_at": str(post.posted_at)[:-6],
        "post_content": post.content,
        "reactions": {
            "count": post.reaction.count(),
            "type": list(dict.fromkeys([p.reaction for p in post.reaction.all()]))
        },
        "comments" : comment_list,
        "comments_count": len(comment_list),
    }
    return res

#task - 13
def get_post(post_id):
    try:
        post = list(Post.objects.select_related('posted_by').prefetch_related('comments', 'reaction', 'comments__reaction','comments__commented_by').filter(id = post_id))[0]
    except:
        #if not Post.objects.filter(pk = post_id).exists():
        raise InvalidPostException
    return get_dict(post)

#Task - 14
def get_user_posts(user_id):
    post = list(
            Post.objects.select_related(
                    'posted_by'
                ).prefetch_related(
                    'comments', 'reaction', 'comments__reaction','comments__commented_by'
                    ).filter(
                            posted_by_id = user_id
                        )
            )
    if not post:
        if not User.objects.filter(pk = user_id).exists():
            raise InvalidUserException
    res_list = []
    for p in post:
        res_list.append(get_dict(p))
    return res_list


#task 15
def get_replies_for_comment(comment_id):
    about_comment=Comment.objects.select_related("commented_by").filter(parent_comment_id=comment_id)
    if not about_comment:
        raise InvalidCommentException
    comment_dict={}
    comment_list=[]
    user_dict={}
    for i in about_comment:
        comment_dict["comment_id"]=i.id
        user_dict["user_id"]=i.commented_by.id
        user_dict["name"]=i.commented_by.name
        user_dict["profile_pic"]=i.commented_by.profile_pic
        comment_dict["commenter"]=user_dict
        comment_dict["commented_at"]=str(i.commented_at)[:-6]
        comment_dict["comment_content"]=i.content
        comment_list.append(comment_dict)
        comment_dict={}
        user_dict={}
    return comment_list
        
    