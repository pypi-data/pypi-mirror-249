

'''
{
	"kind": "projects",
	"fields": {
		"name": "project 1",
		"summary": ""
	}
}
'''

'''
import proceeds.kinds.project as project
project.preset ({
	"name": "",
	"summary": ""
})
'''

from mako.template import Template

import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
border_radius = climate.find () ["layout"] ["border radius"]
repulsion = climate.find () ["layout"] ["repulsion"]
palette = climate.find () ["palette"]

import proceeds.modules.panel as panel

def present (
	fields,
	is_panel = True
):
	name = fields ['name']
	summary = fields ['summary']
	
	if (type (summary) == list):
		summary = "\n".join (summary)
	
	#header = "pack"
	header = "gift"
	
	this_template = f"""
<article
	tile
	style="
		//border: { border_width } solid { palette [3] };
		
		background: { palette [4] };
		border-radius: { border_radius };
		padding: .15in;		
		
		display: flex;
	"
>
	<header
		style="
			display: flex;
		
		"
	>		
		<h1
			style="
				font-style: normal;
			
				text-orientation: upright;
				writing-mode: vertical-rl;
				line-height: 1;
				
				padding: 5px;
				margin-right: 30px;
				border-radius: 4px;
			
				background: { palette [4] };
			"
		>{ header }</h1>	
	</header>
	<section>
		<p><b>{ name }</b></p>
		<p style="white-space: pre-wrap;">{ summary }</p>
	</section>
</article>
	"""
	
	if (is_panel):
		return panel.build (this_template);


	return this_template;
	
	
	
	
	
	
	
#