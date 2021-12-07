import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'

Vue.use(Vuex)


const store = new Vuex.Store({
    state: {
        user: null,
        isAuthenticated: false,
        violations: [],
        webSocketSchemaCount: null,
        allowedFileCount: null,
        wsViolationsCount: null,
        fileViolationsCount: null,
        periodType: 1,
        dates: [],
        chart: {},
        schemas: [],
        callbacks: [],
        wsAllowedOrigins: [],
        filesProxies: [],
        fileInfos: [],
        allowedFiles: [],
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setWebSocketSchemas(state, schemas) {
            state.schemas = schemas;
        },
        setWebSocketCallbacks(state, callbacks) {
            state.callbacks = callbacks;
        },
        setAllowedFiles(state, allowedFiles) {
            state.allowedFiles = allowedFiles;
        },
        setPeriodType(state, periodType) {
            state.periodType = periodType;
        },
        setDates(state, dates) {
            state.dates = dates;
        },
        setChart(state, chartData){
            state.chart = {
                datasets: [
                    {
                        label: 'Websocket Нарушения',
                        borderColor: '#f87979',
                        data: chartData.ws,
                        tension: 0,
                    },
                    {
                        label: 'Файловые нарушения',
                        borderColor: '#0356fc',
                        data: chartData.file,
                        tension: 0,
                    }
                ]
            };
        },
        setViolationsCount(state, count){
            state.wsViolationsCount = count.ws;
            state.fileViolationsCount = count.file;
        },
        setViolations(state, violations){
            state.violations = violations;
        },
        setWebSocketSchemaStat(state, stat) {
            state.webSocketSchemaCount = stat;
        },
        setAllowedFileStat(state, stat) {
            state.allowedFileCount = stat;
        },
        addViolation(state, violation) {
            state.violations.unshift(violation);
        },
        setWsAllowedOrigins(state, data){
            state.wsAllowedOrigins = data;
        },
        setFileProxies(state, data){
            state.filesProxies = data;
        },
        setFileInfo(state, info) {
            state.fileInfos = info;
        }
    },
    actions: {
        async setWebSocketSchemas(context) {
            let response = (await http.getList('WebSocketSchema', {}, true)).data;
            context.commit('setWebSocketSchemas', response);
        },
        async setWebSocketCallbacks(context){
            let response = (await http.getList('WebSocketCallback', {}, true)).data;
            context.commit('setWebSocketCallbacks', response);
        },
        async setWsAllowedOrigins(context){
            let response = (await http.getList('WebSocketAllowedOrigin', {}, true)).data;
            context.commit('setWsAllowedOrigins', response);
        },
        async setFileProxies(context){
            let response = (await http.getList('FileProxy', {}, true)).data;
            context.commit('setFileProxies', response);
        },
        async setAllowedFiles(context){
            let response = (await http.getList('AllowedFile', {}, true)).data;
            context.commit('setAllowedFiles', response);
        },
        async setFileInfo(context){
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let response = (await http.getList('FileInfo', filters, true)).data;
            context.commit('setFileInfo', response);
        },
        async setNewWsAllowedOrigins(context, origins) {
            let prev_origins = context.state.wsAllowedOrigins;
            let new_origins = origins.filter(x => prev_origins.findIndex(v => v.name == x.name) < 0);
            if (new_origins.length){
                for (var new_origin of new_origins){
                    let response = (await http.createItem('WebSocketAllowedOrigin', new_origin, true)).data;
                    prev_origins.push(response)
                }
                context.commit('setWsAllowedOrigins', prev_origins);
                return
            }
            let deleted_origins = prev_origins.filter(x => origins.findIndex(v => v.name == x.name) < 0);
            if (deleted_origins.length){
                for (var deleted_origin of deleted_origins){
                    await http.deleteItem('WebSocketAllowedOrigin', deleted_origin.id, true);
                    let ind = prev_origins.findIndex(x => x.id == deleted_origin.id)
                    prev_origins.splice(ind, 1)
                }
                context.commit('setWsAllowedOrigins', prev_origins);
                return
            }
        },
        async setFilesProxies(context){
            let response = (await http.getList('FilesProxy', {}, true)).data;
            context.commit('setFilesProxies', response);
        },
        async setChart(context) {
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let ws_response = (await http.getList('WSChart', filters, true)).data;
            let files_response = (await http.getList('FileChart', filters, true)).data;
            context.commit('setChart', {ws: ws_response.data, file: files_response.data});
            context.commit('setViolationsCount', {ws: ws_response.count, file: files_response.count});
        },
        async setViolations(context) {
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let response = (await http.getList('Violation', filters, true)).data;
            context.commit('setViolations', response);
        },
        async setWebSocketSchemaStat(context) {
            let response = (await http.getList('WebSocketSchemaStat', {}, true)).data;
            context.commit('setWebSocketSchemaStat', response.count);
        },
        async setAllowedFileStat(context) {
            let response = (await http.getList('AllowedFileStat', {}, true)).data;
            context.commit('setAllowedFileStat', response.count);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var username = creds.username;
            var password = creds.password;
            var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/
            var login_info = {
                email: username,
                password: password
            }
            if (username.match(reg_exp_mail) != null) {
                login_info = {
                    email: username,
                    password: password
                }
            } else {
                login_info = {
                    username: username,
                    password: password
                }
            }
            var status = false;
            try {
                await (Axios.post("/rest_api/auth/login/", login_info, {headers: {'X-CSRFToken': Vue.$cookies.get('csrftoken')}}));
                status = true;
            } catch (error) {
                var data = error.response.data;
                if (data.non_field_errors) {
                    Vue.showErrorModal(data.non_field_errors);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            await Axios.post("/rest_api/auth/logout/", {headers: {'X-CSRFToken': Vue.$cookies.get('csrftoken')}});
            context.commit('setAuthenticated', false);
            context.commit('setUser', {});
        },
        async checkAuth(context) {
            try {
                var result = await Axios.get("/rest_api/auth/user/");
                if (result.status != 200) {
                    context.commit('setUser', {});
                    return
                }
                context.commit('setAuthenticated', true);
                context.commit('setUser', result.data);
            } catch (e) {
                context.commit('setUser', {});
            }
        },
    }
})

export default store;
