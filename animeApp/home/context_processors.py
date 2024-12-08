from main.models import Categories
from django.db.models import Count

class UtilsProcessors:
    def __init__(self, model, method) -> None:
        self.model = model
        self.method = method
        
    
    # def __method__(self):
        

class Processors:
    """
    A class to handle various processor methods, including fetching lists of objects.
    """
    
    def __init__(self) -> None:
        pass
    
    
    """Element removal method"""
    def delete_object(self, model):
        """Delete Element

        Returns:
            model: Model: Модель
        """
        if not model: 
            raise ValueError('Model not provided.')
        
        try:
            model.delete()
        except Exception as e:
            raise e
    
    
    """Get list Init Method"""
    def get_list(self, model, method, filter_empty=False):
        """
        Retrieves a list of objects from the given model based on the specified method.

        Parameters:
        model (Model): The Django model class from which to retrieve the objects.
        method (str): The method type ('list' for fetching all objects).

        Raises:
        ValueError: If the model is None or method is invalid.
        """
        method = method.lower().strip()
        
        if not model:
            raise ValueError('Model not provided.')

        if method == 'list' and isinstance(method, str):
            try:
                if filter_empty:
                    model_list = model.objects.annotate(num_posts=Count('anime')).filter(num_posts__gt=0)
                else:
                    model_list = model.objects.all()
                
                return model_list

            except Exception as e:
                raise Exception(f"An error occurred while retrieving the list: {e}")

        raise ValueError('Invalid method provided.')
            
        
    
    def get_category(self):
        """
        Retrieves the list of categories.

        Parameters:
        request (HttpRequest): The incoming HTTP request.

        Returns:
        dict: A dictionary containing the list of categories.
        """
        categories = self.get_list(Categories, 'list', True)
        
        return {'categories': categories}
    
    
def get_category_func(request):
    """
    Retrieves the list of categories for a view context.
    
    Parameters:
    request (HttpRequest): The incoming HTTP request.
    
    Returns:
    dict: A dictionary containing the list of categories.
    """
    processors = Processors()
    categories = processors.get_category()
    return categories

