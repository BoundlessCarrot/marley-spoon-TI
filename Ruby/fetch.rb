require 'sinatra'
require 'json'
require 'contentful'

def get_credentials
    fp = File.open('credentials.json')
    creds = JSON.parse(fp)

    client = Contentful::Client.new(
        space: creds.space_id, 
        access_token: creds.access_token
    )

    return client

get '/' do
    client = get_credentials
    # recipes = client.entries({"content_type": "recipe"}).select((entry.title, client.asset(entry.photo.id).url(), entry.id))
    recipes = []

    client.entries({"content_type": "recipe"}).each do |entry|
        recipes.append(Array.new(entry.title, client.asset(entry.photo.id).url(), entry.id))
    end

    # erb :recipes, :locals => {'recipes' => recipes}
    @recipes = recipes
    erb :recipes
end

get '/:id' do
    client = get_credentials

    target_entry = client.entry(id)

    tags = []

    begin
        target_entry.tags.each do |tag|
            @tags.append(tag.name.to_s + ", ")
        end
    rescue
        tags = ["No tags available!"]
    end

    begin
        chef = target_entry.fields()['chef'].name
    rescue
        chef = "Chef name unavailable!"
    end

    # erb :detailed_view, :locals => { 'recipe_title' => target_entry.title, 'tags' => tags, 'image' => client.asset(target_entry.photo.id).url, 'description' => markdown(target_entry.description), 'chef' => chef}

    @recipe_title = target_entry.title
    @tags = tags
    @image = client.asset(target_entry.photo.id).url
    @description = markdown(target_entry.description)
    @chef = chef

    erb :detailed_view

end
