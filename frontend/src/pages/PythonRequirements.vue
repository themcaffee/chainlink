<template>
    <div>
        <div class="alert alert-danger" v-if="githubError">
            <button @click="closeGithubError()" type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            Maximum github requests reached. Please login to github to make more requests.
        </div>
        <h1>Python Requirement</h1>
        <form @submit.prevent="getIssues()">
            <div class="form-group">
                <label clas="control-label">Enter requirements.txt here:</label>
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
                <li class="list-group-item" v-for="issue in project['issues']" :key="issue['title']">
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
                githubError: false
            }
        },
        methods: {
            /**
             * Gets a list of issues from the requirements text input
             */
            getIssues () {
                this.getGithubFromPypi(this.requirementsText)
            },
            /**
             * Gets the list of github repos from the REST API
             * @param requirementsText
             */
            getGithubFromPypi (requirementsText)  {
                this.$http.post('http://localhost:5000/api/pypi_github', { 'requirements_text': requirementsText }).then(result => {
                    let repos = result['body']
                    // Get the github issues for each repo
                    for (var repoIndex in repos) {
                        let repo = repos[repoIndex]
                        this.getGithubIssues(repo['owner'], repo['package'])
                    }
                }, errorResult => {
                    // TODO handle errors
                    console.log(errorResult)
                })
            },
            /**
             * Gets the issues for each of the github repos directly from github
             * @param owner
             * @param project
             */
            getGithubIssues (owner, project) {
                if (owner.length === 0 || project.length === 0) {
                    return
                }
                this.$http.get('https://api.github.com/repos/' + owner + '/' + project + '/issues').then(result => {
                    if (result.status === 403) {
                        // The github API has exceeded the maximum amount of requests
                        this.githubError = true
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
            /**
             * Closes the notification that the max github requests has been reached
             */
            closeGithubError () {
                this.githubError = false
            }
        }
    }
</script>
