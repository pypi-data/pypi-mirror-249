from .dtype import *

import sys

class Theme:
    DEFAULT = {'mini_hist_color': '#c7e87c', 'tabset': '#c7e87c','hist_color':'#c7e87c','hist_kde_color':'yellow','bar_color':'#c7e87c','hover_color':'pink'}
    THEME1 = {'hist_color': 'pink', 'tabset': '#7CC7E8','hist_color':'#7CC7E8','hist_kde_color':'pink','bar_color':'#7CC7E8'}
    THEME2 = {'hist_color': 'blue', 'tabset': '#FF5733','hist_color':'#FF5733','hist_kde_color':'blue','bar_color':'#FF5733'}
    # Add more themes as needed
    

class Configs:

    # cache flag
    use_eda_cache = True  
    
    
    # Simple cache to store previously generated plots
    eda_cache = {}

    @classmethod
    def reset_cache(cls, df):
        # Iterate over keys in the cache and remove entries that correspond to the given DataFrame
        keys_to_remove = [key for key in cls.eda_cache.keys() if cls.eda_cache[key]['df'].equals(df)]
        for key in keys_to_remove:
            del cls.eda_cache[key]

        print(f"Cache reset for DataFrame with shape {df.shape}")





    ################################ setting DTYPES #####################################################

    
    dtypes_cache = {}
    dtype = None

    use_id = True
    
    @classmethod
    def get_dtypes(cls, df):
        """Returns a dict of suggested dtypes for each variable"""
        if cls.use_id:
            df_name = id(df)
        else:
            df_name = str(df)
        
        cls.dtype = cls.dtypes_cache.get(df_name,None)   
        
        if cls.dtype is not None:
            return cls.dtypes_cache[df_name]
        else:
            cls.dtypes_cache[df_name] = {i: determine_variable_type(df[i])[0] for i in df.columns}       
        return cls.dtypes_cache[df_name]


    @classmethod
    def set_dtypes(cls,df, dtypes_dict=None):
        """Updates the dtypes attribute with the provided dictionary"""
        if cls.use_id:
            df_name = id(df)
        else:
            df_name = str(df)

        if dtypes_dict == 'reset':
            cls.dtypes_cache[df_name] = None
               
        cls.dtype = cls.dtypes_cache.get(df_name,None)
        
        if cls.dtype is None or dtypes_dict is None:
            cls.dtype = cls.get_dtypes(df)  # Initialize dtypes using get_dtypes if it's None
        else:
            for key, new_value in dtypes_dict.items():
                if key in cls.dtype and cls.dtype[key] != new_value:
                    cls.dtype[key] = new_value
                    cls.dtypes_cache[df_name] = cls.dtype
                    print(cls.dtype)

        return 'done'



    
    ################################ THEME #####################################################
    
    current_theme = Theme.DEFAULT

    @classmethod
    def list_themes(cls, values=True):
        """
        List available themes and their values.

        Parameters:
        - values (bool, optional): If True, returns a dictionary with theme names and values.
          If False, returns a list of theme names only.

        Returns:
        - dict or list: If values is True, a dictionary of theme names and their values.
          If values is False, a list of theme names.
          
        """
        if values:
            themes = {}
            for attr in dir(Theme):
                if not callable(getattr(Theme, attr)) and not attr.startswith("__"):
                    themes[attr] = getattr(Theme, attr)
            return themes
        else:
            return [attr for attr in dir(Theme) if not callable(getattr(Theme, attr)) and not attr.startswith("__")]

    @classmethod
    def set_theme(cls, theme_name):
        """Set the current theme based on the provided theme name."""
        if hasattr(Theme, theme_name):
            cls.current_theme = getattr(Theme, theme_name)
        else:
            print(f"Theme '{theme_name}' not found. Using the default theme.")

    @classmethod
    def add_theme(cls, theme_name, theme_values):
        """
        Add a new theme to the Theme class.
    
        Parameters:
        - cls: The Theme class.
        - theme_name (str): The name of the new theme.
        - theme_values (dict): A dictionary containing the values of the new theme.
    
        Returns:
        - None
    
        Example:
        >>> Configs.add_theme('NEW_THEME', {'hist_color': 'purple', 'tabset': '#FFA500'})
        """
        setattr(Theme, theme_name, theme_values)