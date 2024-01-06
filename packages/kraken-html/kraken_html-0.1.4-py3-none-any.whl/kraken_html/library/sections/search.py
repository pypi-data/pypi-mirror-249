
from kraken_html.library import html

def search(action, theme='light'):
    """Returns a html section for performing search
    """

    # Build search form

    url = action.get('url', None)
    name = action.get('name', None)
    print(url, name)
    
    content = f'''
    
<section>
    <div class="px-4 py-5 my-5 text-center bg-{theme} text-bg-{theme}" data-bs-theme="{theme}" data-aos="fade-down" data-aos-delay="200">

    <form action="{url}" method="post">
    <div class="row">
        <div class="col">
            <input type="text" class="form-control" placeholder="" aria-label="query">
        </div>
            <div class="col">
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </div>
    </form>
    </div>
</section>



</div>
</section>
    
    
    '''

    return content