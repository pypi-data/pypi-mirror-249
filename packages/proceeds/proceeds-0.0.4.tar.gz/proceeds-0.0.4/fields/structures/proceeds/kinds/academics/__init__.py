




import proceeds.kinds.company.status as status

import proceeds.modules.line as line
import proceeds.modules.panel as panel

import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
palette = climate.find () ["palette"]

def introduce (fields, is_panel = True):
	company_name = fields ["name"]
	statuses = fields ["statuses"]
	
	
	start = (
	f"""
<article
	tile
	kind-company
	style="
		// border: { border_width } solid { palette [3] };
		border-radius: .1in;
		padding: .15in;
		margin-bottom: .1in;
		
		display: flex;
	"
>
	<div
		style="
			align-items: baseline;
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
		>🐾 academics</h1>
	</div>
	<div>
		<header
			style="
				display: flex;		
			"
		>
			
			<p
				style="
					text-align: center;
					padding-bottom: .1in;
					font-size: 1.5em;
				"
			>{ company_name }</p>	
		</header>
""")




	end = (f"""</div></article>""")
	
	positions_string = ""
	
	index = 0;
	for _status in statuses:
		positions_string += status.introduce (_status)
		
		if (index < len (statuses) - 1):
			positions_string += line.create ()
			
		index += 1
		
		
		
	content = start + positions_string + end;
	
	if (is_panel):
		return panel.build (content)
		
	return content;