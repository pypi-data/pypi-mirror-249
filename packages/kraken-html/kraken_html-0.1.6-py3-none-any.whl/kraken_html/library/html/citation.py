


def citation(text, author):
    """
    """

    content = f'''
<figure>
    <blockquote class="blockquote">
        <p>{text}</p>
    </blockquote>
    <figcaption class="blockquote-footer">
        <cite title="{author}">
                {author}
        </cite>
    </figcaption>
</figure>

    '''
    return content
