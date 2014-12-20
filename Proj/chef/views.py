from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.contrib.auth import get_user_model
from braces.views import LoginRequiredMixin
from myrecipe.models import Recipe

User = get_user_model()


class PublicChefView(DetailView):
  """
  View a Chef's public profile.
  """
  model = User
  template_name = "chef/chef.html"
  limit_by = 20
  
  def get_context_data(self, **kwargs):
    """
    Provide additional context data about the Chef (public User).
    """
    context = super(PublicChefView, self).get_context_data(**kwargs)
    usr = context["object"]
    context["recentRecipes"] = usr.recipe_set.all()[:self.limit_by]
    return context
  
  def get_object(self):
    return get_object_or_404(User, username = self.kwargs.get("usrname", ""))

  
########################################
# Function to see if user has any recipes with any likes
def UserHasLikes(user):
  for r in user.recipe_set.all():
    if r.likes.exists():
      return True
  return False
########################################

class DashboardView(LoginRequiredMixin, DetailView):
  """
  Render a User's dashboard.
  """
  model = User
  template_name = "chef/dashboard.html"
  limit_by = 10
  
  def get_context_data(self, **kwargs):
    """
    Provide additional context data about the User.
    """
    context = super(DashboardView, self).get_context_data(**kwargs)
    context["recentRecipes"] = self.request.user.recipe_set.all()[:self.limit_by]
    context["recentLikes"] = self.request.user.favoriter.all()[:self.limit_by]
    if UserHasLikes(self.request.user):
      context["ifLikedByAny"] = True
    return context
  
  def get_object(self):
    return None
  
class WhoLiked(LoginRequiredMixin, ListView):
  """
  Only an author can see who liked his/her recipe.
  """
  model = Recipe
  template_name= "chef/wholiked.html"
  paginate_by = 5
  page_kwarg = "page"
  
  def get_queryset(self):
    """
    Return list of each recipe with a sublist of users who liked them
    """
    print "I am " + str(self.request.user.username)
    return self.request.user.recipe_set.all()
  
  
class ChefRecipesList(LoginRequiredMixin, ListView):
  """
  Paginated list of User's created Recipes.
  """
  model = Recipe
  template_name = "chef/chefRecipes.html"
  paginate_by = 5
  page_kwarg = "page"
  
  def get_queryset(self):
    """
    Return the list of 'Favorited' Recipes.
    """
    return self.request.user.recipe_set.all()


class ChefFavoritesList(LoginRequiredMixin, ListView):
  """
  Paginated list of User's favorited Recipes.
  """
  model = Recipe
  template_name = "chef/chefFavorites.html"
  paginate_by = 5
  page_kwarg = "page"
  
  def get_queryset(self):
    """
    Return the list of 'Favorited' Recipes.
    """
    return self.request.user.favoriter.all()

