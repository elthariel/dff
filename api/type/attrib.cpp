#include "attrib.hpp"

Handle::Handle()
{
};

Handle::Handle(dff_ui64 did)
{
  id = did;
};

Handle::Handle(string nname)
{
  name = nname;
};

Handle::Handle(dff_ui64 did, string nname)
{
  id = did;
  name = nname;
};


attrib::attrib() 
{
  size = 0;
};

attrib::~attrib() 
{
};
