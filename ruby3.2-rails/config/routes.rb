Rails.application.routes.draw do
  get '/hello' => 'hello#index', :as => :hello
end
