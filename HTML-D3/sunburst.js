function sunburstChart(chartData) {
	const width = 900;
	const radius = width / 8;

	partition = (data) => {
		const root = d3
			.hierarchy(data)
			.sum((d) => d["Trade Value"])
			.sort((a, b) => b["Trade Value"] - a["Trade Value"]);
		return d3.partition().size([2 * Math.PI, root.height + 1])(root);
	};

	const mainRoot = partition(chartData);
	let root = partition(chartData);

	arc = d3
		.arc()
		.startAngle((d) => d.x0)
		.endAngle((d) => d.x1)
		.padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005))
		.padRadius(radius * 1.5)
		.innerRadius((d) => d.y0 * radius)
		.outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));

	const sectionItems = d3
		.select("#SectionSelectSB")
		.on("change", onchangeSection);

	sectionItems
		.selectAll("#SectionOption")
		.data(mainRoot.children)
		.enter()
		.append("option")
		.text((data) => data.data.name)
		.attr("value", (data) => data.data["Section ID"])
		.attr("class", "SectionOption");

	const svg = d3
		.select("#Sunburst")
		.append("svg")
		.attr("viewBox", [0, 0, width, width])
		.attr("id", "svgSB")
		.style("font", "10px sans-serif");

	const hs2Items = d3.select("#HS2SelectSB");

	function chart() {
		const format = d3.format(",d");
		const color = d3.scaleOrdinal(
			d3.quantize(d3.interpolateRainbow, chartData.children.length + 1)
		);

		root.each((d) => (d.current = d));

		const g = svg
			.append("g")
			.attr("transform", `translate(${width / 2},${width / 2})`);

		const path = g
			.append("g")
			.selectAll("path")
			.data(root.descendants().slice(1))
			.join("path")
			.attr("fill", (d) => {
				while (d.depth > 1) d = d.parent;
				return color(d.data.name);
			})
			.attr("fill-opacity", (d) =>
				arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0
			)
			.attr("d", (d) => arc(d.current));

		path.filter((d) => d.children)
			.style("cursor", "pointer")
			.on("click", clicked);

		path.append("title").text(
			(d) =>
				`${d
					.ancestors()
					.map((d) => d.data.name)
					.reverse()
					.join(" -> ")}\n$${format(d.value)}`
		);

		const label = g
			.append("g")
			.attr("pointer-events", "none")
			.attr("text-anchor", "middle")
			.style("user-select", "none")
			.selectAll("text")
			.data(root.descendants().slice(1))
			.join("text")
			.attr("dy", "0.35em")
			.attr("fill-opacity", (d) => +labelVisible(d.current))
			.attr("transform", (d) => labelTransform(d.current))
			.text((d) => d.data.name);

		const parent = g
			.append("circle")
			.datum(root)
			.attr("r", radius)
			.attr("fill", "none")
			.attr("pointer-events", "all")
			.on("click", clicked);

		hs2Items.on("change", onchangeHS2);

		function clicked(event, p) {
			parent.datum(p.parent || root);

			root.each(
				(d) =>
					(d.target = {
						x0:
							Math.max(
								0,
								Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))
							) *
							2 *
							Math.PI,
						x1:
							Math.max(
								0,
								Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))
							) *
							2 *
							Math.PI,
						y0: Math.max(0, d.y0 - p.depth),
						y1: Math.max(0, d.y1 - p.depth),
					})
			);

			const t = g.transition().duration(750);

			// Transition the data on all arcs, even the ones that aren’t visible,
			// so that if this transition is interrupted, entering arcs will start
			// the next transition from the desired position.
			path.transition(t)
				.tween("data", (d) => {
					const i = d3.interpolate(d.current, d.target);
					return (t) => (d.current = i(t));
				})
				.filter(function (d) {
					return (
						+this.getAttribute("fill-opacity") ||
						arcVisible(d.target)
					);
				})
				.attr("fill-opacity", (d) =>
					arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0
				)
				.attrTween("d", (d) => () => arc(d.current));

			label
				.filter(function (d) {
					return (
						+this.getAttribute("fill-opacity") ||
						labelVisible(d.target)
					);
				})
				.transition(t)
				.attr("fill-opacity", (d) => +labelVisible(d.target))
				.attrTween("transform", (d) => () => labelTransform(d.current));
		}

		function arcVisible(d) {
			return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
		}

		function labelVisible(d) {
			return (
				d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03
			);
		}

		function labelTransform(d) {
			const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
			const y = ((d.y0 + d.y1) / 2) * radius;
			return `rotate(${x - 90}) translate(${y},0) rotate(${
				x < 180 ? 0 : 180
			})`;
		}

		function onchangeHS2() {
			let selectValue1 = d3.select("#HS2SelectSB").property("value");
			let selectedHS2;

			root.children.forEach((element) => {
				if (element.data["HS2 ID"] == selectValue1) {
					selectedHS2 = element;
				}
			});
			clicked(null, selectedHS2);
		}

		return svg.node();
	}

	function onchangeSection() {
		let selectValue = d3.select("#SectionSelectSB").property("value");
		let selectedSection;
		let HS2Options;

		chartData.children.forEach((element) => {
			if (element["Section ID"] == selectValue) {
				selectedSection = element;
				HS2Options = element.children;
			}
		});

		d3.selectAll("#svgSB > *").remove();
		root = partition(selectedSection);
		setHS2(HS2Options);
		chart();
	}

	function setHS2(data) {
		d3.selectAll("#HS2SelectSB > *").remove();
		hs2Items
			.selectAll("#HS2OptionSB")
			.data(data)
			.enter()
			.append("option")
			.text((data) => data.name)
			.attr("value", (data) => data["HS2 ID"])
			.attr("class", "HS2OptionSB");
	}

	chart();
}
