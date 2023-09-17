<script>
	let role = 0;
	let card = 1;
	import welcome_fallback from '$lib/images/svelte-welcome.png';
</script>

<div class="card" style="margin: auto;">
	<img src={welcome_fallback} alt="Avatar" style="width:100%">
	<div class="container">
	  <h4><b>Jane Doe</b></h4> 
	  <p>Interior Designer</p> 
	</div>
</div>
  

<style>
	.card {
	  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
	  transition: 0.3s;
	  width: 40%;
	  border-radius: 5px;
	  background: #8d59f4;
	}
	
	.card:hover {
	  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
	}
	
	img {
	  border-radius: 5px 5px 0 0;
	}
	
	.container {
	  padding: 2px 16px;
	}
</style>