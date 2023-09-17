<script>
	let role = 0;
	export let eventNo;
	export let eventStr;

	let array = eventStr.split(";");
</script>

<div class="event">
	{#each array as el, idx}
		<h3>{el}</h3>
	{/each}
</div>

<style>

	h3 {
		color:white;
	}

</style>
