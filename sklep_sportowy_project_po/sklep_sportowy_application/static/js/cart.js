var updatebutton=document.getElementsByClassName('update-cart')

for (var i=0; i<updatebutton.length; i++){
    updatebutton[i].addEventListener('click', function (){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:', action)

        console.log('USER', user)
        if(user ==='AnonymousUser'){
            console.log('Not logged')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}