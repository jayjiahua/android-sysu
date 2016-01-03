# -*- coding: utf-8 -*-
# !/usr/bin/env python


from utils.db import Base, engine
import models.student
import models.moment

#student_table = Student.__table__
# moment_table = Moment.__table__
# moment_like_table = MomentLike.__table__
# moment_unlike_table = MomentUnlike.__table__

metadata = Base.metadata

metadata.create_all(engine)
