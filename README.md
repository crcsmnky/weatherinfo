# What's the Weather?

This is a sample app meant for use with Kubernetes and/or Istio. It displays the weather from a single city (Austin, TX) or multiple cities (Austin, New York, San Francisco, Seattle).

## Building

The images can be built using [Docker](http://docker.com) or using [Cloud Build](http://cloud.google.com/cloud-build). To build an invidual image, refer to the following example:

`gcloud builds submit --tag gcr.io/[PROJECTID]/weather-frontend:1.0 frontend/`

Or to build all of the images, run `build-images.sh`.

## Deploying

There are deployment specifications for Kubernetes and Istio in `manifests`. Before proceeding, you will need an API key from [OpenWeatherMap](http://openweathermap.org/api).

Once you have your API key, add a `Secret` to your Kubernetes cluster:
- `kubectl create secret generic openweathermap --from-literal=apikey=[OPENWEATHERMAP-API-KEY]`

### Kubernetes

To deploy the app to Kubernetes (without Istio), use the following commands:
- `kubectl apply -f manifests/weather-deployment.yaml`

*Note*: the Services are not externally accessible (no Ingress resource is created) so to access `weather-frontend` you'll need to use port forwarding and open [http://localhost:5000](http://localhost:5000):
- `kubectl port-forward deployment/weather-frontend 5000:5000`

### Kubernetes and Istio

Once you have created a Kubernetes cluster and installed Istio, you can deploy the sample app as follows.

First, enable auto-injection of the Envoy `istio-proxy`:
- `kubectl label ns default istio-injection=enabled`

Then deploy the rules first and the app second:
- `kubectl apply -f manifests/weather-rules.yaml`
- `kubectl apply -f manifests/weather-deployment.yaml`

Now grab the `istio-ingressgateway` Load Balancer IP address:
- `INGRESSGATEWAY=$(kubectl get svc -n istio-system istio-ingressgateway -o jsonpath="{.status.loadBalancer.ingress..ip}")`
- Open `http://$INGRESSGATEWAY` in a browser

*Note:* If you do not want to enable auto-injection of `istio-proxy` for the `default` namespace, you can also use `istioctl` to include `istio-proxy` in your Pods:
- `kubectl apply -f <(istioctl kube-inject -f manifests/weather-deployment.yaml)`

## Generating Load

This repo also contains a [Locust](http://locust.io) script to generate load against `weather-frontend`. 

**IMPORTANT**
- The `loadgenerator` deployment is set to hit `weather-frontend.default:5000` and not `$INGRESSGATEWAY` therefore the traffic is coming from within the cluster
- The `loadgenerator` is configured as a single replica with `5` clients randomly generating requests every 1-5s. *Keep this in mind so you don't go over your OpenWeatherMap API Key quota*.

To deploy `loadgenerator`, update `FRONTEND_HOST` in `manifests/loadgen.yaml` and then apply:
- `kubectl apply -f manifests/loadgen.yaml`
