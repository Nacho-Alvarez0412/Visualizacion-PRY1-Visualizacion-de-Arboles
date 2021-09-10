function icicleChartTB(chartData) {
	var width = document.querySelector("#IcicleTB").offsetWidth,
		height = 500;

	const format = d3.format(",d");
	const color = d3.scaleOrdinal(
		d3.quantize(d3.interpolateRainbow, chartData.children.length + 1)
	);

	let root = d3
		.hierarchy(chartData)
		.sum((d) => d["Trade Value"])
		.sort(function (a, b) {
			return b["Trade Value"] - a["Trade Value"];
		});

	var x = d3.scaleLinear().range([0, width]);

	var y = d3.scaleLinear().range([0, height]);

	var partition = d3.partition().size([width, height]).padding(1).round(true);

	partition(root);

	var svg = d3
		.select("#IcicleTB")
		.append("svg")
		.attr("width", width)
		.attr("height", height)
		.attr("id", "svgTB")
		.style("font", "15px sans-serif");

	const sectionItems = d3
		.select("#SectionSelectTB")
		.on("change", onchangeSection);

	sectionItems
		.selectAll("#SectionOptionTB")
		.data(root.children)
		.enter()
		.append("option")
		.text((data) => truncateTxt(data.data.name))
		.attr("value", (data) => data.data["Section ID"])
		.attr("class", "SectionOptionTB");

	const hs2Items = d3.select("#HS2SelectTB");

	function chart() {
		const cell = svg.selectAll("g").data(root.descendants()).join("g");

		var rect = cell.append("rect");

		rect = rect
			.attr("x", (d) => d.x0)
			.attr("y", (d) => d.y0)
			.attr("width", (d) => d.x1 - d.x0)
			.attr("height", (d) => d.y1 - d.y0)
			.attr("fill-opacity", 0.6)
			.attr("fill", (d) => {
				if (!d.depth) return "#ccc";
				while (d.depth > 1) d = d.parent;
				return color(d.data.name);
			})
			.style("cursor", "pointer")
			.on("click", clicked);
		/*
        const text = cell.append("text")
            .style("user-select", "none")
            .attr("pointer-events", "none")
            .attr("x", d => d.x0 + 10)
            .attr("y", d => d.y0 + 40)
            .attr("fill-opacity", d => +labelVisible(d));

        text.append("tspan")
            .text(d => d.data.name);

        const tspan = text.append("tspan")
            .attr("fill-opacity", d => labelVisible(d) * 0.7)
        */

		cell.append("title").text(
			(d) =>
				`${d
					.ancestors()
					.map((d) => d.data.name)
					.reverse()
					.join(" -> ")}\n Trade Value: $${format(d.value)}`
		);

		hs2Items.on("change", onchangeHS2);

		function clicked(event, p) {
			focus = focus === p ? (p = p.parent) : p;

			x.domain([p.x0, p.x1]);
			y.domain([p.y0, height]).range([p.depth ? 20 : 0, height]);

			const t = rect
				.transition()
				.duration(750)
				.attr("x", function (d) {
					return x(d.x0);
				})
				.attr("y", function (d) {
					return y(d.y0);
				})
				.attr("width", function (d) {
					return x(d.x1) - x(d.x0);
				})
				.attr("height", function (d) {
					return y(d.y1) - y(d.y0);
				});
			//text.transition(t).attr("fill-opacity", d => +labelVisible(d.target));
			//tspan.transition(t).attr("fill-opacity", d => labelVisible(d.target) * 0.7);
		}

		function labelVisible(d) {
			return d.y1 <= width && d.y0 >= 0 && d.x1 - d.x0 > 16;
		}

		function onchangeHS2() {
			let selectValue1 = d3.select("#HS2SelectTB").property("value");
			let selectedHS2;

			root.children.forEach((element) => {
				if (element.data["HS2 ID"] == selectValue1) {
					selectedHS2 = element;
				}
			});
			clicked(null, selectedHS2);
		}
	}

	function onchangeSection() {
		let selectValue = d3.select("#SectionSelectTB").property("value");
		let selectedSection;
		let HS2Options;

		chartData.children.forEach((element) => {
			if (element["Section ID"] == selectValue) {
				selectedSection = element;
				HS2Options = element.children;
			}
		});

		d3.selectAll("#svgTB > *").remove();

		root = d3
			.hierarchy(selectedSection)
			.sum((d) => d["Trade Value"])
			.sort(function (a, b) {
				return b["Trade Value"] - a["Trade Value"];
			});

		partition(root);
		chart();

		setHS2(HS2Options);
	}

	function setHS2(data) {
		d3.selectAll("#HS2SelectTB > *").remove();
		hs2Items
			.selectAll("#HS2OptionTB")
			.data(data)
			.enter()
			.append("option")
			.text((data) => truncateTxt(data.name))
			.attr("value", (data) => data["HS2 ID"])
			.attr("class", "HS2Option");
	}

	chart();

	function truncateTxt(text) {
		if (text.length > 40) {
			return text.slice(0, 40) + "...";
		} else {
			return text;
		}
	}
}
