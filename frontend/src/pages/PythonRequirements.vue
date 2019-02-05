<template>
    <div>
        <div class="alert alert-danger" v-if="githubError">
            <button @click="closeGithubError()" type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            Maximum github requests reached. Please login to github to make more requests.
        </div>
        <h1>Chainlink <small>Python Requirements</small></h1>
        <a :href="'https://github.com/login/oauth/authorize?client_id=' + githubClientID">Sign in with Github</a>
        <form @submit.prevent="getIssues()">
            <div class="form-group">
                <label clas="control-label">requirements.txt</label>
                <textarea v-model="requirementsText" class="form-control" rows="10"></textarea>
            </div>
            <button class="btn btn-default pull-right" type="submit">Get issues</button>
        </form>
        <div class="panel panel-default" v-for="project in issues" :key="project['project']">
            <div class="panel-heading">
                <div class="page-heading">
                    <h3>Project: {{ project['project'] }} - Owner: {{ project['owner'] }}</h3>
                </div>
            </div>
            <ul class="list-group">
                <li class="list-group-item" v-for="issue in project['issues']">
                    <a :href="issue['url']">{{ issue['title'] }} </a>
                    <small class="pull-right">{{ issue['created_at'] }}</small>
                </li>
                <li class="list-group-item" v-if="project['issues'].length === 0">No issues found</li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                requirementsText: '',
                issues: [],
                githubClientID: '',
                githubError: false
            }
        },
        methods: {
            getIssues () {
                this.getGithubFromPypi(this.requirementsText)
            },
            getGithubFromPypi (requirementsText)  {
                this.$http.post('http://localhost:5000/api/pypi_github', { 'requirements_text': requirementsText }).then(result => {
                    let repos = result['body']
                    for (var repoIndex in repos) {
                        let repo = repos[repoIndex]
                        this.getGithubIssues(repo['owner'], repo['package'])
                    }
                }, errorResult => {
                    // TODO handle errors
                    console.log(errorResult)
                })
            },
            getGithubIssues (owner, project) {
                if (owner.length === 0 || project.length === 0) {
                    return
                }
                this.$http.get('https://api.github.com/repos/' + owner + '/' + project + '/issues').then(result => {
                    if (result.status === 403) {
                        this.githubError = false
                        console.log('Getting github issues failed :(')
                    } else if (result.status === 200) {
                        let newProject = {
                            "owner": owner,
                            "project": project,
                            "issues": result['body']
                        }
                        this.issues.push(newProject)
                    }
                }, errorResult => {
                    // TODO handle errors
                    console.log(errorResult)
                })
            },
            closeGithubError () {
                this.githubError = false
            }
        }
    }
</script>
