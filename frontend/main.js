
$.fn.wrapBy = function (tag = "div") {
    return $(`<${tag}></${tag}>`).append(this);
}

const data = {};

function get(url, data = {}, method = "GET") {
    const BASE_URL = `http://${window.location.hostname}:5000/api`;
    method = method.toUpperCase();
    url = (Object.keys(data) == 0 || method != "GET") ? url : url + "?" + Object.entries(data).map(([k, v]) => `${k}=${v}`).join("&");

    return new Promise((resolve, reject) => {
        fetch(BASE_URL + url, {
            method,
            body: method != "GET" ? JSON.stringify(data) : undefined
        })
        .then(res => res.json())
        .then(r => {
            console.log(url, r);
            resolve(r);
        })
        .catch(reject);
    })
}

async function get2(url, data = {}, method = "GET") {
    try {
        $("button").prop("disabled", true);
        return await get(url, data, method);
    }
    finally {
        $("button").prop("disabled", false);
    }
}

function round(x, n = 2) {
    return Math.round(x*(10**n))/(10**n);
}

function hideAll() {
    $("#root > *").hide();
}

function $btn(text, type = "primary") {
    return $(`<button type="button" class="btn btn-${type}">${text}</button>`)
}

function $loading() {
    return $(`<div>
        <div style="padding: 60px;">
            <div class="spinner-border text-primary" role="status">
                ${false ? "" : '<span class="sr-only" style="padding-left: 12px">Loading...</span>'}
            </div>
        </div>
    </div>`);
}

function $table({ headers, items, title = "", subtitle = "", LIMIT = 5 }) {
    const $table = $(`<div class="card">
        <div class="card-body">
            ${title ? `<h3>${title}</h3>` : ""}
            ${subtitle ? `<h6>${subtitle}</h6>` : ""}
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        ${headers.map(h => `<th scope="col">${h.text}</th>`).join("")}
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <h6 class="mb-4 table-info"></h6>
            <div class="table-control"></div>
        </div>
    </div>`);

    function render(start = 0, limit = LIMIT) {
        $table.find(".table-control").html("");
        let i;
        for (i = start; i < start + limit && i < items.length; i++) {
            $table.find("table tbody").append(
                $("<tr></tr>").append(
                    $(`<th scope="row">${i + 1}</th>`),
                    headers.map(h => {
                        try {
                            return $(`<td>${items[i][h.value]}</td>`);
                        }
                        catch(e) {
                            console.error("Error message:", e.message);
                            console.error("Stack trace:", e.stack);
                            console.log(i, h, h.value, items[i]);
                        }
                    })
                )
            );
        }
        if (i < items.length) {
            $table.find(".table-control").append(
                $btn(`Xem thêm ${LIMIT}`).on("click", () => render(i)),
                $btn("Xem tất cả").addClass("ml-3").on("click", () => render(i, 10e10))
            );
        } else {
            $table.find(".table-info").html("");
        }
    }
    $table.find(".table-info").html("Tổng số bản ghi: " + items.length);
    render();

    return $table;
}

function $tableGroup({ tables, LIMIT = 5, perRow = 2 }) {
    const $tableGroup = $(`<div>
        <div class="tables row gy-4"></div>
        <h6 class="mb-4 mt-3 table-group-info"></h6>
        <div class="table-group-control"></div>
    </div>`);

    function render(start = 0, limit = LIMIT) {
        $tableGroup.find(".table-group-control").html("");
        let i;
        for (i = start; i < start + limit && i < tables.length; i++) {
            $tableGroup.find(".tables").append(
                $table({ ...tables[i], LIMIT: 10e10 }).wrapBy().addClass("col-" + (12/perRow))
            );
        }
        if (i < tables.length) {
            $tableGroup.find(".table-group-control").append(
                $btn(`Xem thêm ${LIMIT}`).on("click", () => render(i)),
                $btn("Xem tất cả").addClass("ml-3").on("click", () => render(i, 10e10))
            );
        } else {
            $tableGroup.find(".table-group-info").html("");
        }
    }
    $tableGroup.find(".table-group-info").html("Tổng số bản ghi: " + tables.length);
    render();

    return $tableGroup;
}

const studentHeaders = [
    { value: "name", text: "Tên" },
    { value: "academic_year", text: "Khóa" },
    { value: "major", text: "Lĩnh vực ngành học" },
    { value: "social_style", text: "Tính cách xã hội" },
    { value: "bedtime_habit", text: "Giờ đi ngủ" },
    { value: "religion", text: "Tôn giáo" },
    { value: "average_monthly_spending", text: "Chi tiêu hàng<br>tháng (VNĐ)" },
    { value: "is_smoker", text: "Hút thuốc" },
    { value: "sports_passion", text: "Đam mê thể thao" },
    { value: "music_passion", text: "Đam mê nhạc" },
    { value: "gaming_passion", text: "Đam mê game" }
];

const roomHeaders = [
    { value: "room_name", text: "Tên phòng" },
    { value: "building_name", text: "Tòa nhà" },
    { value: "capacity", text: "Sức chứa" }
];

async function home() {
    hideAll();
    const $home = $("#root div#home").show().html("").append(
        $('<div class="col-12"></div>').append(
            $btn("Gán nhãn dữ liệu", "info").on("click", labelData),
            $btn("Phân chia phòng", "success").addClass("ml-3").on("click", result)
        )
    );

    $home.append(
        $table({
            headers: studentHeaders,
            items: [],
            title: "Danh sách Sinh viên"
        })
        .wrapBy().prop("id", "temp-student-table"),
        $table({
            headers: roomHeaders,
            items: [],
            title: "Danh sách Phòng"
        })
        .wrapBy().addClass("col-md-6").prop("id", "temp-room-table"),
    );
    
    const { rooms, student_requests: students, weights } = await get2("/");
    data.rooms = rooms;
    data.students = students;
    data.roomMapping = {};
    data.studentMapping = {};
    data.rooms.forEach(room => data.roomMapping[room.id] = room);
    data.students.forEach(student => data.studentMapping[student.student_id] = student);
    data.weights = weights;

    $home.find("#temp-student-table").remove().end()
        .find("#temp-room-table").remove().end()
        .append(
            $table({
                headers: studentHeaders,
                items: students,
                title: "Danh sách Sinh viên"
            })
            .wrapBy(),
            $table({
                headers: roomHeaders,
                items: rooms,
                title: "Danh sách Phòng"
            })
            .wrapBy().addClass("col-md-6"),
            '<div class="col-md-6" id="room-capacity-statistic"></div>'
        );

    chart({
        id: "room-capacity-statistic",
        data: data.rooms.map(room => room.capacity),
        xlabel: "Sức chứa của phòng",
        ylabel: "Số phòng",
        title: "Thống kê về sức chứa của phòng"
    })
}
home();

async function labelData() {
    hideAll();
    const sumWeights = Object.values(data.weights).reduce((p, v) => p + v);
    const weights = studentHeaders.filter(({value}) => data.weights[value] !== undefined).map(
        ({ text, value }) => ({ text: text.replaceAll("<br>", " "), value, weight: Math.round(data.weights[value]*10/sumWeights*100)/100 })
    );
    const $tab = $("#label-data").show().html("").append(
        $("<div></div>").append(
            $btn("Quay lại").on("click", home)
        ),
        $('<div class="row gy-4 mt-4 mb-3"></div>').append(
            $('<ul class="list-group"></ul>').append(
                weights.map(({ text, weight }) => {
                    return $(`<li class="list-group-item">
                        <div class="d-flex justify-content-between">
                            <div class="fw-bold">${text}</div>
                            <span>${weight}</span>
                        </div>
                    </li>`);
                })
            ).wrapBy().addClass("col-md-6"),
            '<div id="weights-statistic" class="col-md-6"></div>'
        )
    );
    const weights2 = {};
    weights.forEach(({ text, weight }) => weights2[text] = weight);
    chart({
        id: "weights-statistic",
        data: weights2,
        xlabel: "Thuộc tính",
        ylabel: "",
        title: "Thống kê về trọng số"
    });
    const { student_requests: students } = await get("/");
    const LIMIT = 10;
    const score = {};

    for (let i = 0; i < LIMIT && i < students.length; i++) {
        const ri = () => Math.round(Math.random() * students.length);
        const i1 = ri();
        let i2 = ri();
        while (i2 == i1) i2 = ri();
        $tab.append(
            $("<div></div>").append(
                $table({
                    headers: studentHeaders,
                    items: [students[i1], students[i2]]
                }),
                $('<div class="mt-3 mb-5"></div>').append((() => {
                    const r = [];
                    const name = "name" + i1 + i2 + ri();
                    for (let i = 0; i < 11; i++) {
                        const id = "id" + Math.round(Math.random() * 10e10);
                        const label = {
                            0: "0 (Rất hợp nhau)",
                            10: "10 (Rất khác biệt)"
                        }
                        r.push($(`<div class="form-check form-check-inline mr-5">
                            <input class="form-check-input" type="radio" id=${id} name="${name}">
                            <label class="form-check-label" for="${id}">${label[i] || i}</label>
                        </div>`)
                        .find("input").on("change", function () {
                            if (this.checked) score[i1 + "-" + i2] = i;
                        }).end());
                    }
                    return r;
                })())
            )
        );
    }

    function getResult() {
        const r = [];
        Object.entries(score).forEach(([k, v]) => {
            const [id1, id2] = k.split("-").map(i => students[i].student_id);
            r.push({
                std1: data.studentMapping[id1],
                std2: data.studentMapping[id2],
                dis: v
            });
        });
        return r;
    }

    async function saveLabeledData() {
        await get2("/labeled_data", getResult(), "post");
    }

    $tab.append(
        $("<div></div>").append(
            $btn("Lưu dữ liệu", "success").on("click", async () => {
                await saveLabeledData();
                home();
            }),
            $btn("Export kết quả", "info").addClass("ml-3").on("click", async () => {
                const blob = new Blob([JSON.stringify(getResult())], { type: "text/plain" });
                const a = document.createElement("a");
                a.href = URL.createObjectURL(blob);
                a.download = `he-tro-giup-quyet-dinh-gan-nhan-${Math.round(Math.random() * 10e10)}.txt`;
                a.click();
                URL.revokeObjectURL(a.href);
                await saveLabeledData();
                home();
            }),
            $btn("Quay lại").addClass("ml-3").on("click", home)
        )
    );
}

async function result() {
    hideAll();
    const $result = $("#result").html("").show().append(
        $('<div class="col-12"></div>').append(
            $btn("Quay lại").on("click", home)
        )
    );

    const deltaTimeStr = (t1, t2 = -1) => {
        if (t2 < 0) t2 = new Date().getTime();
        const delta = (t2 - t1)/1000;
        const text = delta < 60 ? `${Math.round(delta*10)/10}s` : `${Math.floor(delta/60)}m ${Math.floor(delta - Math.floor(delta/60)*60)}s`;
        return text;
    }

    const $step1 = $('<div class="row gy-4 mt-3"></div>').append(
        $(`<h2>Bước 1: Phân chia ${data.students.length} sinh viên thành ${data.rooms.length} cụm <span id="kmean-step1-time"></span></h2>`),
        $loading().prop("id", "kmean-loading"),
        `<div id="kmean-result" style="display: none">
            <div class="row gy-3 mt-3">
                <div class="col-md-6" id="kmean-step1-mde-statistic"></div>
                <div class="col-md-6" id="kmean-step1-room-num-students-statistic"></div>
                <div class="col-md-12" id="kmean-step1-room-and-cluster-num-students-statistic" style="max-height: 500px;"></div>
            </div>
            <select class="form-select mt-4" style="width: max-content;">
                <option value="1" selected>Sắp xếp theo Sự khác biệt của sinh viên trong cụm tăng dần</option>
                <option value="2">Sắp xếp theo Sự khác biệt của sinh viên trong cụm giảm dần</option>
                <option value="3">Sắp xếp theo số sinh viên trong cụm tăng dần</option>
                <option value="4">Sắp xếp theo số sinh viên trong cụm giảm dần</option>
            </select>
            <div class="row gy-3 mt-3" id="kmean-result-groups"></div>
        </div>`
    )
    .appendTo($result);
    const t1 = new Date().getTime();

    const interval1 = setInterval(() => {
        $step1.find("#kmean-step1-time").html(`(${deltaTimeStr(t1)})`);
    }, 100);

    const { id, result } = await get("/k-means-result");
    const [studentIdsLists, MEDs] = result;
    const clusters = [];
    for (let i = 0; i < studentIdsLists.length; i++) {
        clusters.push({
            studentIds: studentIdsLists[i],
            med: MEDs[i]
        });
    }

    const avg = arr => arr.reduce((p, v) => p + v, 0)/arr.length;
    $step1.find("#kmean-step1-statistic-wrapper").append(
        $btn("Xem thống kê", "success").wrapBy().on("click", function () {
            $(this).parent().append(
                '<div class="col-md-6" id="kmean-step1-mde-statistic"></div>',
                '<div class="col-md-6" id="kmean-step1-room-num-students-statistic"></div>',
                '<div class="col-md-12" id="kmean-step1-room-and-cluster-num-students-statistic"></div>'
            );
            $(this).remove();

            chart({
                id: "kmean-step1-mde-statistic",
                data: MEDs,
                xlabel: "Độ khác biệt",
                ylabel: "Số lượng cụm",
                title: `Thống kê về độ khác biệt trung bình của các cụm (avg: ${round(avg(MEDs))})`,
                binCount: 40
            });
        
            chart({
                id: "kmean-step1-room-num-students-statistic",
                data: studentIdsLists.map(i => i.length),
                xlabel: "Số sinh viên",
                ylabel: "Số lượng cụm",
                title: "Thống kê về số sinh viên trong các cụm",
                paddingInteger: true,
                binCount: 10e10
            });
        
            chart2({
                id: "kmean-step1-room-and-cluster-num-students-statistic",
                title: "Thống kê về số sinh viên trong các cụm và sức chứa của các phòng",
                data1: {
                    data: data.rooms.map(i => i.capacity),
                    label: "Sức chứa phòng"
                },
                data2: {
                    data: studentIdsLists.map(i => i.length),
                    label: "Số sinh viên trong cụm"
                }
            });
        })
    )

    clearInterval(interval1);

    $step1.find("#kmean-loading").remove();
    $step1.find("#kmean-result").show();

    $step1.find("select").on("change", function () {
        const mode = this.value;

        const cp = (a, b) => {
            if (mode == 1) return a.med - b.med;
            else if (mode == 2) return b.med - a.med;
            else if (mode == 3) return a.studentIds.length - b.studentIds.length;
            else if (mode == 4) return b.studentIds.length - a.studentIds.length;
            return 0;
        };

        const cl = [...clusters];
        cl.sort(cp);

        renderKmeanResults(cl);
    })
    .trigger("change");

    function renderKmeanResults(clusters) {
        $step1.find("#kmean-result-groups").html("").append(
            $tableGroup({
                tables: clusters.map(({ studentIds, med }, i) => ({
                    headers: studentHeaders.filter(({ value }) => value != "name"),
                    items: studentIds.map(id => data.studentMapping[id]),
                    title: `Cụm ${i + 1}`,
                    subtitle: `Độ khác biệt trung bình: ${Math.round(med*100)/100}`
                })),
                LIMIT: 2,
                perRow: window.innerWidth < 1300 ? 1 : 2
            })
            .wrapBy()
        );
    }

    const $step2 = $('<div class="row gy-4 mt-4"></div>').append(
        $(`<h2>Bước 2: Phân chia các cụm sinh viên về các phòng <span id="kmean-step2-time"></span></h2>`),
        $loading().prop("id", "kmean-step2-loading"),
        `<div id="kmean-step2-result" style="display: none">
            <div class="row gy-3 mt-3">
                <div class="col-md-12" id="kmean-step2-mde-statistic"></div>
            </div>
            <select class="form-select mt-4" style="width: max-content;">
                <option value="1" selected>Sắp xếp theo Sự khác biệt của sinh viên trong phòng tăng dần</option>
                <option value="2">Sắp xếp theo Sự khác biệt của sinh viên trong phòng giảm dần</option>
                <option value="3">Sắp xếp theo số sinh viên trong phòng tăng dần</option>
                <option value="4">Sắp xếp theo số sinh viên trong phòng giảm dần</option>
            </select>
            <div class="row gy-3 mt-3" id="kmean-step2-result-groups"></div>
        </div>`
    )
    .appendTo($result);
    const t2 = new Date().getTime();

    const interval2 = setInterval(() => {
        $step2.find("#kmean-step2-time").html(`(${deltaTimeStr(t2)})`);
    }, 100);

    const { result: result2 } = await get("/allocation-result", { id });
    const roomsStudents = [];
    result2.forEach(r => {
        roomsStudents.push({
            roomId: r["room_id"],
            studentIds: r["student_ids"],
            med: r["med"]
        })
    });
    clearInterval(interval2);

    $step2.find("#kmean-step2-statistic-wrapper").append(
        $btn("Xem thống kê", "success").wrapBy().on("click", function () {
            $(this).parent().append(
                '<div class="col-md-6" id="kmean-step2-mde-statistic"></div>'
            );
            $(this).remove();

            chart3({
                id: "kmean-step2-mde-statistic",
                data1: {
                    data: roomsStudents.map(i => i.med),
                    label: `Sau bước 2 (avg: ${round(avg(roomsStudents.map(i => i.med)))})`
                },
                data2: {
                    data: MEDs,
                    label: `Sau bước 1 (avg: ${round(avg(MEDs))})`
                },
                xlabel: "Độ khác biệt",
                ylabel: "Số lượng phòng",
                title: "Thống kê về độ khác biệt trung bình của các phòng",
                binCount: 50
            });
        })
    );

    $step2.find("#kmean-step2-loading").remove();
    $step2.find("#kmean-step2-result").show();

    $step2.find("select").on("change", function () {
        const mode = this.value;

        const cp = (a, b) => {
            if (mode == 1) return a.med - b.med;
            else if (mode == 2) return b.med - a.med;
            else if (mode == 3) return a.studentIds.length - b.studentIds.length;
            else if (mode == 4) return b.studentIds.length - a.studentIds.length;
            return 0;
        };

        const rs = [...roomsStudents];
        rs.sort(cp);

        renderKmeanStep2Results(rs);
    })
    .trigger("change");

    function renderKmeanStep2Results(roomsStudents) {
        $step2.find("#kmean-step2-result-groups").html("").append(
            $tableGroup({
                tables: roomsStudents.map(({ studentIds, med, roomId }) => ({
                    headers: studentHeaders.filter(({ value }) => value != "name"),
                    items: studentIds.map(id => data.studentMapping[id]),
                    title: `Phòng ${data.roomMapping[roomId].room_name}`,
                    subtitle: `Độ khác biệt trung bình: ${Math.round(med*100)/100}`
                })),
                LIMIT: 2,
                perRow: window.innerWidth < 1300 ? 1 : 2
            })
            .wrapBy()
        );
    }
}

function chart({ id, data, xlabel, ylabel = "Số lượng", title = "", binCount = 20, paddingInteger = false, objectDataSortValue = true }) {
    let x, y;

    const isNumber = s => {
        const s2 = parseFloat(s);
        if (!isNaN(s2)) {
            return true;
        }
        return false;
    }
    const toSorted = arr => {
        arr = [...arr];
        if (arr.every(s => isNumber(s))) {
            arr.sort((a, b) => parseInt(a) - parseInt(b));
        }
        else {
            arr.sort();
        }
        return arr;
    }

    const paddingIntegerArray = arr => {
        arr = arr.map(i => parseInt(i));
        const min = Math.min(...arr);
        const max = Math.max(...arr);
        const r  = [];
        for (let i = min; i <= max; i++) {
            r.push(String(i));
        }
        return r;
    }

    if (Array.isArray(data)) {
        const set = [...new Set(data)];
        const allIsNumber = set.every(s => isNumber(s));
        if (set.length < binCount || (!allIsNumber)) {
            x = toSorted(set);
            if (paddingInteger && allIsNumber) {
                x = paddingIntegerArray(x);
            }

            const o = {};
            data.forEach(i => {
                if (!o[i]) o[i] = 1;
                else o[i]++;
            });

            y = x.map(i => o[i] || 0);
        }
        else {
            const minValue = Math.min(...data);
            const maxValue = Math.max(...data);
            const binSize = (maxValue - minValue) / binCount;

            x = [];
            y = [];
            for (let i = 0; i < binCount; i++) {
                const t = minValue + binSize*(0.5 + i);
                x.push(Math.round(t*100)/100);
                y.push(0);
            }

            data.forEach(value => {
                const binIndex = Math.min(
                    Math.floor((value - minValue) / binSize),
                    x.length - 1
                );
                y[binIndex]++;
            });
        }
    }
    else {
        x = toSorted(Object.keys(data));
        if (paddingInteger) x = paddingIntegerArray(x);
        y = x.map(i => data[i] || 0);

        if (objectDataSortValue) {
            const idx = y.map((_, i) => i);
            idx.sort((a, b) => y[a] - y[b]);
            y = idx.map(i => y[i]);
            x = idx.map(i => x[i]);
        }
    }

    const canvas = document.createElement("canvas");
    document.getElementById(id).appendChild(canvas);
    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: x,
            datasets: [{
                label: ylabel,
                data: y,
                backgroundColor: "#1f77b4"
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: xlabel
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: ylabel
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                ...(title ? {
                    title: {
                        display: true,
                        text: title,
                        font: {
                            size: 18,
                        },
                        padding: {
                            top: 10,
                            bottom: 10,
                        },
                    },
                } : {})
            }
        }
    });
}

function chart2({ id, data1, data2, ylabel, title = "" }) {
    const handle = data => {
        const x = data.map((_, i) => i);
        const y = [...data];
        y.sort((a, b) => parseInt(a) - parseInt(b));
        return [x, y];
    };

    const [x1, y1] = handle(data1.data);
    const [x2, y2] = handle(data2.data);

    const canvas = document.createElement("canvas");
    document.getElementById(id).appendChild(canvas);
    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: x1,
            datasets: [{
                label: data1.label,
                data: y1,
                backgroundColor: "#1f77b4"
            }, {
                label: data2.label,
                data: y2,
                backgroundColor: "#ff6384"
            }]
        },
        options: {
            barPercentage: 1,
            categoryPercentage: 1,
            scales: {
                x: {
                    title: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: ylabel
                    }
                }
            },
            plugins: {
                ...(title ? {
                    title: {
                        display: true,
                        text: title,
                        font: {
                            size: 18,
                        },
                        padding: {
                            top: 10,
                            bottom: 10,
                        },
                    },
                } : {})
            }
        }
    });
}

function chart3({ id, data1, data2, xlabel = "Số lượng", ylabel, title = "", binCount = 20 }) {
    const minVal = Math.min(...data1.data, ...data2.data);
    const maxVal = Math.max(...data1.data, ...data2.data);
    const binSize = (maxVal - minVal) / binCount;

    const x = [], y1 = [], y2 = [];
    for (let i = 0; i < binCount; i++) {
        const t = minVal + binSize*(0.5 + i);
        x.push(Math.round(t*10)/10);
        y1.push(0);
        y2.push(0);
    }

    [data1.data, data2.data].forEach((data, i) => {
        data.forEach(value => {
            const binIndex = Math.min(
                Math.floor((value - minVal) / binSize),
                x.length - 1
            );
            if (i == 0) y1[binIndex]++;
            else y2[binIndex]--;
        });
    });

    const canvas = document.createElement("canvas");
    document.getElementById(id).appendChild(canvas);
    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: x,
            datasets: [{
                label: data1.label,
                data: y1,
                backgroundColor: "#1f77b4"
            }, {
                label: data2.label,
                data: y2,
                backgroundColor: "#ff6384"
            }]
        },
        options: {
            scales: {
                x: {
                    stacked: true,
                    title: {
                        display: true,
                        text: xlabel
                    }
                },
                y: {
                    stacked: true,
                    title: {
                        display: true,
                        text: ylabel
                    },
                    ticks: {
                        callback: v => Math.abs(v)
                    }
                }
            },
            plugins: {
                ...(title ? {
                    title: {
                        display: true,
                        text: title,
                        font: {
                            size: 18,
                        },
                        padding: {
                            top: 10,
                            bottom: 10,
                        },
                    },
                } : {})
            }
        }
    });
}
