float 10000roses[10000*3];
bool first=true;
void r3d_glColorPointer(GLint size, GLenum type, GLsizei stride, const
GLvoid *pointer)
{
  R3DR3D_PROLOG(ColorPointer);
  R3D_TRACEGL(("ColorPointer(size %d type 0x%x stride %u pointer 0x%lx
)\n", (int)size, (unsigned int)type, (unsigned int)stride, (unsigned
long)pointer));

  // bidouille rose
  size=3;
  type=GL_FLOAT;
  float rose[3]={255,200,200};
  if(first)
  {
          first=false;
          int i;
          for(i=0;i<10000;i++)
                  memcpy(&10000roses[3*i],rose,3*sizeof(float));
  }
  stride=24;
  pointer=10000roses;
