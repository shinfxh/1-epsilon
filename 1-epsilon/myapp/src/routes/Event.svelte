<script>
	let role = 0;
	export let eventNo;
</script>

{#if eventNo == 1}

<div class="event">
	<h3>
	Person X color-shared with Person Y.
	</h3>
</div>
{:else if eventNo == 2}

<div class="event">
	<h3>
	Person X full-shared with Person Y.
	</h3>
</div>

{:else }

<div class="event">
	<h3>
	Person X is voted off.
	</h3>
</div>


{/if}



<style>

	h3 {
		color:white;
	}

</style>
