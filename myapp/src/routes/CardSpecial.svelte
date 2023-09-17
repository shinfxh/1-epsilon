<script>
	export let role;
	export let name;
	import welcome_fallback from '$lib/images/user1.png';
</script>

<div class="cardspecial" style="margin: auto;">
	<img src={welcome_fallback} alt="Avatar">
	<div class="container">
	  <h4><b>{name}</b></h4> 
	  <p>{role}</p> 
	</div>
</div>
  

<style>
	.cardspecial {
	  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
	  transition: 0.3s;
	  min-width: 40px;
	  border-radius: 5px;
	  text-align: center;
	  max-height: 40px;
	}

	h4 {
		color: white;
	}
	p {
		color: white;
	}
	
	.cardspecial:hover {
	  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
	}
	
	img {
	  border-radius: 5px 5px 0 0;
	  margin: auto;
	}
	
	.container {
	  padding: 2px 16px;
	}
</style>