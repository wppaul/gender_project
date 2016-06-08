class DemoController < ApplicationController
  layout "project"
  
  def club_shopping
      @boxes= ["club", "shopping"]
  end

  def afl_clubs
  end

  def time_tweet
  	  @time= ["week","day"]
  end

  def top_name
  	  @gender=['male','female']
  end

  def postcode
    @data_feature={
      "overview"=>"Overview",
      "people"=>"People", 
      "male"=>"Male", 
      "female"=>"Female",
    }
  end
  def heat_map
    @heat_gender={"male"=>"Find the male cluster","female"=>"Find the female cluster"}
  end

  def scatter
  end
end
