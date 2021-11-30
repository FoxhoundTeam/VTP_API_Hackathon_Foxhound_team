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
        httpAllowedTypeCount: null,
        violationsCount: null,
        periodType: 1,
        dates: [],
        chart: {},
        schemas: [],
        callbacks: [],
        wsAllowedOrigins: [],
        filesProxies: [],
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
        setHTTPAllowedTypes(state, types) {
            state.httpAllowedTypes = types;
        },
        setPeriodType(state, periodType) {
            state.periodType = periodType;
        },
        setDates(state, dates) {
            state.dates = dates;
        },
        setChart(state, chart){
            state.chart = {
                datasets: [
                    {
                        label: 'Нарушения',
                        borderColor: '#f87979',
                        data: chart,
                        tension: 0,
                    }
                ]
            };
        },
        setViolationsCount(state, violationsCount){
            state.violationsCount = violationsCount;
        },
        setViolations(state, violations){
            state.violations = violations;
        },
        setWebSocketSchemaStat(state, stat) {
            state.webSocketSchemaCount = stat;
        },
        setHTTPAllowedTypeStat(state, stat) {
            state.httpAllowedTypeCount = stat;
        },
        addViolation(state, violation) {
            state.violations.unshift(violation);
        },
        setWsAllowedOrigins(state, data){
            state.wsAllowedOrigins = data;
        },
        setFilesProxies(state, data){
            state.filesProxies = data;
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
        async setNewFilesProxies(context, proxies) {
            let prev_proxies = context.state.filesProxies;
            let new_proxies = proxies.filter(x => prev_proxies.findIndex(v => v.proxy_url == x.proxy_url) < 0);
            if (new_proxies.length){
                for (var new_proxy of new_proxies){
                    let response = (await http.createItem('FilesProxy', new_proxy, true)).data;
                    prev_proxies.push(response)
                }
                context.commit('setFilesProxies', prev_proxies);
                return
            }
            let deleted_proxies = prev_proxies.filter(x => proxies.findIndex(v => v.proxy_url == x.proxy_url) < 0);
            if (deleted_proxies.length){
                for (var deleted_proxy of deleted_proxies){
                    await http.deleteItem('FilesProxy', deleted_proxy.id, true);
                    let ind = prev_proxies.findIndex(x => x.id == deleted_proxy.id)
                    prev_proxies.splice(ind, 1)
                }
                context.commit('setFilesProxies', prev_proxies);
                return
            }
        },
        async setFilesProxies(context){
            let response = (await http.getList('FilesProxy', {}, true)).data;
            context.commit('setFilesProxies', response);
        },
        async setChart(context) {
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let response = (await http.getList('Chart', filters, true)).data;
            context.commit('setChart', response.data);
            context.commit('setViolationsCount', response.count);
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
        async setHTTPAllowedTypeStat(context) {
            let response = (await http.getList('HTTPAllowedTypeStat', {}, true)).data;
            context.commit('setHTTPAllowedTypeStat', response.count);
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
