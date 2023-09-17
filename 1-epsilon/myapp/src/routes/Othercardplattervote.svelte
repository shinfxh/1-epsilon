<script>
	let role = 0;
	let card = 1;
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Othercard from './Othercard.svelte';
	export let namesList;

</script>

<div class="othercardplattervote">
	<div id = "leftbox">
		<Othercard name={namesList[0]}/>
	</div>
	 
	<div id = "middlebox">
		<Othercard name={namesList[1]}/>
	</div>
	 
	<div id = "rightbox">
		<Othercard name={namesList[2]}/>
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