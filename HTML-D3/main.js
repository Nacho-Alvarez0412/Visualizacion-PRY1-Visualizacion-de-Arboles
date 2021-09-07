async function main() {
    CHART_DATA = await getData();
    icicleChartLR (CHART_DATA);
}

main();