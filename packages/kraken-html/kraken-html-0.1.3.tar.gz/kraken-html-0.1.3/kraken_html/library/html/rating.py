

def rating(ratingValue):
    """Returns a star rating
    """

    if not isinstance(ratingValue, (int, float)):
        return ''
    
    if ratingValue > 5 and ratingValue <= 10:
        ratingValue = ratingValue / 2

    if ratingValue > 10:
        ratingValue = ratingValue / 10
    
    content = ''
    count = 0
    
    while count < int(ratingValue):
        content += '<i class="bi bi-star-fill text-warning"  fill="currentColor" ></i>'
        count += 1


    if int(ratingValue) != ratingValue:
        content += '<i class="bi bi-star-half text-warning" fill="currentColor" ></i>'
        count += 1
    
    
    while count < 5:
        content += '<i class="bi bi-star text-warning" fill="currentColor" ></i>'
        count += 1
       
    return content