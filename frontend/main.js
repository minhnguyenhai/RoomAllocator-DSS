
$.fn.wrapBy = function (tag = "div") {
    return $(`<${tag}></${tag}>`).append(this);
}

const data = {};

function get(url, params = {}) {
    const BASE_URL = "http://localhost:5000/api";
    url = Object.keys(params) == 0 ? url : url + "?" + Object.entries(params).map(([k, v]) => `${k}=${v}`).join("&");

    return new Promise((resolve, reject) => {
        fetch(BASE_URL + url).then(res => res.json()).then(resolve).catch(reject);
    })
}

function hideAll() {
    $("#root > *").hide();
}

function $btn(text) {
    return $(`<button type="button" class="btn btn-primary">${text}</button>`)
}

function $loading() {
    return $(`<div>
        <div style="padding: 60px;">
            <div class="spinner-border text-primary" role="status">
                ${true ? "" : '<span class="sr-only" style="padding-left: 12px">Loading...</span>'}
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
                        return $(`<td>${items[i][h.value]}</td>`);
                    })
                )
            );
        }
        if (i < items.length) {
            $table.find(".table-control").append(
                $btn(`Xem thêm ${LIMIT}`).on("click", () => render(start + LIMIT)),
                $btn("Xem tất cả").addClass("ml-3").on("click", () => render(start + LIMIT, 10e10))
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
                $btn(`Xem thêm ${LIMIT}`).on("click", () => render(start + LIMIT)),
                $btn("Xem tất cả").addClass("ml-3").on("click", () => render(start + LIMIT, 10e10))
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
            $btn("Gán nhãn dữ liệu").on("click", labelData),
            $btn("Phân chia phòng").addClass("ml-3").on("click", result)
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

    const { rooms, student_requests: students } = await get("/");
    data.rooms = rooms;
    data.students = students;
    data.roomMapping = {};
    data.studentMapping = {};
    data.rooms.forEach(room => data.roomMapping[room.id] = room);
    data.students.forEach(student => data.studentMapping[student.student_id] = student);

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
            .wrapBy().addClass("col-md-6")
        );
}
home();

async function labelData() {
    hideAll();
    const $tab = $("#label-data").show().html("").append(
        $("<div></div>").append(
            $btn("Quay lại").on("click", home)
        )
    );
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
                        r.push($(`<div class="form-check form-check-inline mr-5">
                            <input class="form-check-input" type="radio" id=${id} name="${name}">
                            <label class="form-check-label" for="${id}">${i}</label>
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

    $tab.append(
        $("<div></div>").append(
            $btn("Export kết quả").on("click", () => {
                const r = [];
                Object.entries(score).forEach(([k, v]) => {
                    const [id1, id2] = k.split("-").map(i => students[i].student_id);
                    r.push({
                        std1: data.studentMapping[id1],
                        std2: data.studentMapping[id2],
                        dis: v
                    });
                });

                const blob = new Blob([JSON.stringify(r)], { type: "text/plain" });
                const a = document.createElement("a");
                a.href = URL.createObjectURL(blob);
                a.download = `he-tro-giup-quyet-dinh-gan-nhan-${Math.round(Math.random() * 10e10)}.txt`;
                a.click();
                URL.revokeObjectURL(a.href);
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

    const $step1 = $('<div class="row mt-3"></div>').append(
        $(`<h2>Bước 1: Phân chia ${data.students.length} sinh viên thành ${data.rooms.length} cụm <span id="kmean-step1-time"></span></h2>`),
        $loading().prop("id", "kmean-loading"),
        `<div id="kmean-result" style="display: none">
            <select class="form-select" style="width: max-content;">
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
    let a = 0;
    for (let i = 0; i < studentIdsLists.length; i++) {
        clusters.push({
            studentIds: studentIdsLists[i],
            med: MEDs[i]
        });
        a += studentIdsLists[i].length;
    }
    console.log(id, a);

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

    const $step2 = $('<div class="row mt-4"></div>').append(
        $(`<h2>Bước 2: Phân chia các cụm sinh viên về các phòng <span id="kmean-step2-time"></span></h2>`),
        $loading().prop("id", "kmean-step2-loading"),
        `<div id="kmean-step2-result" style="display: none">
            <select class="form-select" style="width: max-content;">
                <option value="1" selected>Sắp xếp theo Sự khác biệt của sinh viên trong cụm tăng dần</option>
                <option value="2">Sắp xếp theo Sự khác biệt của sinh viên trong cụm giảm dần</option>
                <option value="3">Sắp xếp theo số sinh viên trong cụm tăng dần</option>
                <option value="4">Sắp xếp theo số sinh viên trong cụm giảm dần</option>
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
