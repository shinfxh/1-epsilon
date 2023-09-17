<script>
	let role = 0;
	let card = 1;
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Othercardvote from './Othercardvote.svelte';
	export let namesList;
	export let fn1;
	export let fn2;
	export let fn3;
</script>

<div class="othercardplattervote">
	<div id = "leftbox">
		<Othercardvote fn={fn1} name={namesList[0]}/>
	</div>
	 
	<div id = "middlebox">
		<Othercardvote fn={fn2} name={namesList[1]}/>
	</div>
	 
	<div id = "rightbox">
		<Othercardvote fn={fn3} name={namesList[2]}/>
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