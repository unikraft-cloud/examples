class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
end

class HelloController < ApplicationController
  def index
    @text = "Hello, World!"
  end
end
