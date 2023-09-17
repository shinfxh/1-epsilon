<script>
	let role = 0;
	let card = 1;
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Othercard from './Othercard.svelte';

</script>

<div class="othercardplattervote">
	<div id = "leftbox">
		<Othercard/>
	</div>
	 
	<div id = "middlebox">
		<Othercard/>
	</div>
	 
	<div id = "rightbox">
		<Othercard/>
	</div>
</div>
  

<style>
	#leftbox {
		float:left;
		width:33%;
		height:280px;
	}
	#middlebox{
		float:left;
		width:33%;
		height:280px;
	}
	#rightbox{
		float:right;
		width:33%;
		height:280px;
	}
	
	img {
	  border-radius: 5px 5px 0 0;
	}
	
	.container {
	  padding: 2px 16px;
	}
</style>