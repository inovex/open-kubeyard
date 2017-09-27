require 'colorize'

namespace :kubeyard do

  desc 'Init gcloud and k8s deployment'
  task init: ['gcloud:init', 'k8s:init', 'helm:init']

  desc 'Install helm chart'
  task install: ['helm:install']

  desc 'Upgrade release'
  task upgrade: ['helm:upgrade']

end

namespace :gcloud do

  desc 'Init gcloud'
  task init: ['gcloud:create_cluster', 'gcloud:connect_to_cluster']

  desc 'Create a gcloud cluster'
  task :create_cluster do
    cluster_name = ENV['cluster_name'] || 'kubeyard'
    abort('Missing env var cluster_name'.colorize(:red)) if cluster_name.to_s.empty?
    puts "Creating cluster #{cluster_name} if not existing".colorize(:green)
    if not cluster_name == `gcloud container clusters list --format 'get(name)'`.strip!
      sh "gcloud container clusters create '#{cluster_name}'"
    end
  end

  desc 'Connect to gcloud cluster'
  task :connect_to_cluster do
    project_name = ENV['project_name'] || `gcloud config list --format 'value(core.project)'`.strip!
    abort('Missing env var project_name'.colorize(:red)) if project_name.to_s.empty?
    cluster_name = ENV['cluster_name'] || 'kubeyard'
    abort('Missing env var cluster_name'.colorize(:red)) if cluster_name.to_s.empty?
    puts "Connecting to cluster #{cluster_name}".colorize(:green)
    sh "gcloud container clusters get-credentials '#{cluster_name}' --zone europe-west1-b --project '#{project_name}'"
  end

  desc 'Delete a gcloud cluster'
  task :delete_cluster do
    cluster_name = ENV['cluster_name'] || 'kubeyard'
    abort('Missing env var cluster_name'.colorize(:red)) if cluster_name.to_s.empty?
    puts "Deleting cluster #{cluster_name}".colorize(:green)
    sh "gcloud container clusters delete -q '#{cluster_name}'"
  end

end

namespace :k8s do

  desc 'Init k8s'
  task init: ['k8s:set_context', 'k8s:create_namespace', 'k8s:create_secret']

  desc 'Set kubectl context'
  task :set_context do
    puts "Setting kubectl context".colorize(:green)
    project_name = `gcloud config list --format 'value(core.project)'`.strip!
    sh "kubectl config set-context $(kubectl config current-context)"
    sh "kubectl config use-context $(kubectl config current-context)"
  end

  desc 'Create namespace kubeyard'
  task :create_namespace do
    puts "Creating namespace kubidata if not existing".colorize(:green)
    namespace = `kubectl get namespace | grep kubeyard | sed 's/ .*//'`.strip!
    if not namespace == 'kubeyard'
      sh "kubectl create namespace kubeyard"
    end
  end

  desc 'Add secret to default service account'
  task :create_secret do
    puts "Creating new secret to access docker registry with service account".colorize(:green)
    username = ENV['username']
    abort('Missing env var username'.colorize(:red)) if username.to_s.empty?
    token = ENV['token']
    abort('Missing env var token'.colorize(:red)) if token.to_s.empty?
    email = ENV['email']
    abort('Missing env var email'.colorize(:red)) if email.to_s.empty?
    namespace = ENV['namespace'] || 'kubeyard'
    puts "Using namespace: #{namespace}".colorize(:green)

    secret_key = `kubectl get secrets --namespace=#{namespace} | grep inovex-gitlab-registry-key | sed 's/ .*//'`.strip!
    if not secret_key == "inovex-gitlab-registry-key"
      puts "Create new secret for docker registy in namespace #{namespace}".colorize(:green)
      sh "kubectl create secret docker-registry inovex-gitlab-registry-key --docker-server=registry.inovex.de:4567 --docker-username=#{username} --docker-password=#{token} --docker-email=#{email} --namespace=#{namespace}"
    end
    puts "Add secret to kubernetes default service account in namespace #{namespace}".colorize(:green)
    sh <<-SCRIPT
      kubectl get serviceaccounts default -o json --namespace=#{namespace} | jq  'del(.metadata.resourceVersion)'| jq 'setpath(["imagePullSecrets"];[{"name":"inovex-gitlab-registry-key"}])' | kubectl replace serviceaccount default -f - --namespace=#{namespace}
    SCRIPT
  end

end

namespace :helm do

  helm_charts_basedir = './helm'
  pkgs = FileList["#{helm_charts_basedir}/**/*.tgz"]
  helm_min_version = Gem::Version.new('2.3.0')

  desc 'Init helm'
  task init: ['helm:check_version'] do
    puts 'Initializing helm'.colorize(:green)
    sh 'helm init'
    puts "List available services on all namespaces".colorize(:green)
    sh "while test -z \"$(kubectl get svc --all-namespaces | awk 'NR>1 {print $2}' | grep '^tiller-deploy$')\"; do sleep 2; done;"
  end

  desc 'Check helm version'
  task check_version: [] do
    puts "Check helm version".colorize(:green)
    helm_version = Gem::Version.new(`helm version -c --short | sed 's/.*v\\(.*\\)\\+.*/\\1/'`)
    abort("Helm >= #{helm_min_version} is required".colorize(:red)) if helm_version < helm_min_version
  end

  desc 'Build helm packages'
  task pkg: ['helm:check_version'] do
    puts '(Re-)Generating helm chart repo'.colorize(:green)

    puts "Package components without requirements".colorize(:green)
    Dir.foreach(helm_charts_basedir) do |item|
      path_to_chart = "./helm/" + item + "/Chart.yaml"
      if item.include? 'helm' and File.exist?(path_to_chart)
        path_to_requirements = "./helm/" + item + "/requirements.yaml"
        if not File.exist?(path_to_requirements)
          sh "helm package #{helm_charts_basedir}/#{item}"
        end
      end
    end
    sh 'rm -rf ./helm/charts'
    sh 'mkdir ./helm/charts'
    sh 'mv *.tgz ./helm/charts'
    sh 'helm repo index ./helm/charts'

    puts "Update dependencies of components with requirements and package them".colorize(:green)
    Dir.foreach(helm_charts_basedir) do |item|
      path_to_chart = "./helm/" + item + "/Chart.yaml"
      if item.include? 'helm' and File.exist?(path_to_chart)
        path_to_requirements = "./helm/" + item + "/requirements.yaml"
        path_to_dir = "./helm/" + item
        if File.exist?(path_to_requirements)
          sh "helm dep update #{path_to_dir}"
          sh "helm package #{helm_charts_basedir}/#{item}"
        end
      end
    end
    sh 'mv *.tgz ./helm/charts'
    sh 'helm repo index ./helm/charts'

    puts "Update dependencies of apps".colorize(:green)
    Dir.foreach('./apps') do |item|
      path_to_chart = "./apps/" + item + "/Chart.yaml"
      if File.exist?(path_to_chart)
        path_to_requirements = "./apps/" + item + "/requirements.yaml"
        puts path_to_requirements
        path_to_dir = "./apps/" + item
        if File.exist?(path_to_requirements)
          sh "helm dep update #{path_to_dir}"
        end
      end
    end
  end

  desc 'Install helm release'
  task install: ['helm:check_version', 'helm:pkg'] do
    puts "Installing helm release".colorize(:green)
    namespace = ENV['namespace'] || 'kubeyard'
    chart = ENV['chart']
    abort('Missing env var chart'.colorize(:red)) if chart.to_s.empty?

    helm_opts = []
    helm_opts << '--debug' if ENV['helm_debug'] == 'true'

    install_opts = []
    install_opts << '--dry-run' if ENV['helm_debug'] == 'true'

    puts "Installing chart #{chart} to namespace #{namespace}".colorize(:green)
    sh "helm #{helm_opts.join(' ')} install #{install_opts.join(' ')} \ #{chart}"
  end

  desc 'Upgrade helm release'
  task upgrade: ['helm:check_version', 'helm:pkg'] do
    puts "Upgrading helm release".colorize(:green)
    namespace = ENV['namespace'] || 'kubeyard'
    release = ENV['release'] || `helm list --date --reverse -q --max 1`.strip!
    chart = ENV['chart']
    abort('Missing env var chart'.colorize(:red)) if chart.to_s.empty?

    helm_opts = []
    helm_opts << '--debug' if ENV['helm_debug'] == 'true'

    release_opts = []
    release_opts << '--dry-run' if ENV['helm_debug'] == 'true'

    puts "Upgrading release #{release}".colorize(:green)

    sh "helm #{helm_opts.join(' ')} upgrade #{release} #{release_opts.join(' ')} \ #{chart}"
  end

  desc 'Remove all generated helm files'
  task clean: ['helm:check_version'] do
    rm pkgs
    rm "#{helm_charts_basedir}/charts/index.yaml"
  end

end
