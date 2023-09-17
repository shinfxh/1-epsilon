<script>
	let role = 0;
	let card = 1;
	import welcome_fallback from '$lib/images/test.png';
	import Chatbox from './Chatbox.svelte';

    async function approach() {
        // Make the API Call here
		console.log("approached me!");
    }
    let visible = false;

    function toggleVissible() {
        visible = !visible
    }

	export let fn;
	export let name;
</script>

<div class="othercard">
	<img src={welcome_fallback} alt="Avatar" style="width:100%">
	<div class="container">
	  <h4><b>{name}</b></h4> 
	  {#if fn == null}
	  {:else}
	  	<button on:click={fn}>Approach</button>
	  {/if}
	</div>
</div>

{#if visible}
<Chatbox/>
{/if}

<style>
	button {
		margin: auto;
		display:block;
	}
	.othercard {
	  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
	  transition: 0.3s;
	  min-width: 40px;
	  border-radius: 5px;
	}

	h4 {
		color:rgb(255, 255, 255);
		text-align: center;
	}
	
	.othercard:hover {
	  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
	}
	
	img {
	  border-radius: 5px 5px 0 0;
	  margin: auto;
	  display:block;
	}
	
	.container {
	  padding: 2px 16px;
	}
</style>